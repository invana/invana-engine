from invana.server.gql import GremlinQuery
from graphene import Schema
import json
import os

schema = Schema(query=GremlinQuery)


class TestGraphQuery:

    @staticmethod
    def test_create_vertex():
        # label = "Planet"
        # properties = json.dumps({
        #     "name": "Earth",
        #     "human_population": "a lot"
        # })
        results = schema.execute("""
            query {
                vertexCreate(properties: "{\\"name\\": \\"Earth\\"}", label: "Planet")
            }
        """)
        print("results", results)
        # assert results.data == {"vertexCreate": "{\"name\": \"Earth\"}"}
