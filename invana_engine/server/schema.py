#  Copyright 2021 Invana
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http:www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# CREDITS - https://stackoverflow.com/a/52690104
from invana_engine.modeller.query import ModellerQuery
from invana_engine.graph.query import GraphSchema
import graphene

class_definition_example = [{
    "id": "author",
    "name": "BookAuthor",
    "desc": "Book author information",
    "options": [
        {
            "id": "name",
            "label": "author name",
            "type": "text",
            "required": True,
            "placeholder": "author name here"
        }
    ]
}]


def make_resolver(record_name, record_cls):
    def resolver(self, info):
        print("resolve##################, ", self, info, record_name , record_name)
        data = "Hello"
        return record_cls(data)

    resolver.__name__ = 'resolve_%s' % record_name
    return resolver


field_types = {
    'text': graphene.String,
    # ...
}


def create_schema_dynamically():
    record_schemas = {}
    for record_type in class_definition_example:
        classname = record_type["id"]  # 'Author'
        fields = {}
        for option in record_type["options"]:
            field_type = field_types[option['type']]
            print("============field_type", field_type)
            fields[option['id']] = field_type()  # maybe add label as description

            print("====fields", fields)
            rec_cls = type(
                classname,
                (graphene.ObjectType,),
                fields,
                name=record_type['name'],
                description=record_type['desc'],
            )
            record_schemas[record_type['id']] = rec_cls
    # create Query in similar way
    print("===============record_schemas", record_schemas)
    fields = {}
    for key, rec in record_schemas.items():
        fields[key] = graphene.Field(rec)
        fields['resolve_%s' % key] = make_resolver(key, rec)
    Query = type('Query', (graphene.ObjectType,), fields)

    return graphene.Schema(query=Query, types=list(record_schemas.values()))


class Query(ModellerQuery, GraphSchema):
    pass


# Query = create_schema_dynamically()
