from invana_engine2.invana.gremlin.connector import GremlinConnector
from .management import  JanusGraphGraphManagement


class JanusGraphConnector(GremlinConnector):
        management_cls = JanusGraphGraphManagement
        
