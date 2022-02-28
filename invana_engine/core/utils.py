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
import graphene


def convert_to_graphql_schema(schema_items):
    graphql_schema_items = []
    for schema_item in schema_items:
        graphql_schema_item = {
            'id': schema_item['name'],  # slugify
            'name': schema_item['name'],
            'desc': f"browse {schema_item['name']}",
            'options': []
        }
        for property_data in schema_item['properties']:
            graphql_schema_item['options'].append({
                "id": property_data["name"],
                "label": property_data["name"],
                "type": property_data["type"],
                "required": None,
                "placeholder": f'{property_data["name"]} here'
            })
        graphql_schema_items.append(graphql_schema_item)
    return graphql_schema_items


