#  Copyright 2020 Invana
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http:www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import logging
from invana_engine.utils.chores import import_klass
from invana_engine.default_settings import GREMLIN_SERVER_SETTINGS as GREMLIN_SERVER_DEFAULT_SETTINGS
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from .operations.vertex import VertexOperations
from .operations.edge import EdgeOperations
from .operations.schema import SchemaOperations
from .operations.stats import GraphStatsOperations
from invana_engine.auth import BasicAuth, TokenAuth
import ast

logger = logging.getLogger(__name__)


class GremlinClient:

    def __init__(self, gremlin_server_url, traversal_source=None, serializer_class=None, auth=None):
        if gremlin_server_url is None:
            gremlin_server_url = GREMLIN_SERVER_DEFAULT_SETTINGS['gremlin_url']
            logging.info("No gremlin_server_url provided by user. using default value '{}'".format(gremlin_server_url))
        if traversal_source is None:
            traversal_source = GREMLIN_SERVER_DEFAULT_SETTINGS['traversal_source']
            logging.info("No traversal_source provided by user. using default value '{}'".format(traversal_source))
        if serializer_class is None:
            serializer_class_str = GREMLIN_SERVER_DEFAULT_SETTINGS['serializer_class']
            logging.info("No serializer_class provided by user. using default serializer class '{}'".format(
                serializer_class_str))
            serializer_class = import_klass(serializer_class_str)
        if auth is not None:
            self.validate_auth_type(auth)

        self.gremlin_server_url = gremlin_server_url
        self.traversal_source = traversal_source
        self.serializer = serializer_class()
        self.auth = auth
        self.connection = self.create_connection()
        self.g = traversal().withRemote(self.connection)
        self.vertex = VertexOperations(gremlin_client=self)
        self.edge = EdgeOperations(gremlin_client=self)
        self.schema = SchemaOperations(gremlin_client=self)
        self.stats = GraphStatsOperations(gremlin_client=self)

    @staticmethod
    def validate_auth_type(auth):
        if isinstance(auth, BasicAuth) and isinstance(auth, TokenAuth):
            raise Exception("auth should be of BasicAuth or TokenAuth type")

    def create_connection(self):
        driver_extra_params = {}
        if self.auth:
            driver_extra_params = self.auth.get_driver_params()
        return DriverRemoteConnection(
            self.gremlin_server_url,
            self.traversal_source,
            **driver_extra_params
        )

    @staticmethod
    def make_data_unique(serialize_data):
        _ids = []
        unique_data = []
        for serialize_datum in serialize_data:
            if type(serialize_datum) is dict and serialize_datum.get("id"):
                if serialize_datum['id'] not in _ids:
                    _ids.append(serialize_datum['id'])
                    unique_data.append(serialize_datum)
            else:
                unique_data.append(serialize_datum)
        return unique_data

    def query(self, gremlin_query, serialize_elements=True):
        logger.info("Executing query : {}".format(gremlin_query))
        try:
            result = self.connection._client.submit(gremlin_query).all().result()
        except Exception as e:
            logger.error("Failed to query gremlin server with exception: {}".format(e.__str__() if e else ""))
            return None
        if serialize_elements is True:
            _ = self.make_data_unique(self.serializer.serialize_data(result))
            if isinstance(result, list):
                return _
            else:
                return _[0]
        return result

    def get_graph_features(self):
        _ = self.query("graph.features()")[0]
        result = {}
        this_feature_name = None
        _ = _.replace("FEATURES", "")
        for feature_section in _.split("> "):
            for feature_section_item in feature_section.split("\n"):
                if feature_section_item:
                    if not feature_section_item.startswith(">--"):
                        this_feature_name = feature_section_item.strip()
                        result[this_feature_name] = {}
                    else:
                        feature_name = feature_section_item.split(":")[0].lstrip(">--").rstrip()
                        feature_status = feature_section_item.split(":")[1].strip()
                        result[this_feature_name][feature_name] = ast.literal_eval(feature_status.capitalize())
        return result

    def close_connection(self):
        self.connection.close()
