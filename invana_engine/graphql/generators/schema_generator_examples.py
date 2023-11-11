from .ariadne_generator import AriadneGraphQLSchemaGenerator
import asyncio



def example_schema_with_subscription():
    type_def = """
        type Query {
            _unused: Boolean
        }
        
        type Mutation {
            _unused: Boolean
        }

        type Subscription {
            counter: Int!
        }
    """
    schema_generator = AriadneGraphQLSchemaGenerator()
 
    @schema_generator.subscription.source("counter")
    async def counter_generator(obj, info):
        for i in range(50):
            await asyncio.sleep(1)
            yield i

    @schema_generator.subscription.field("counter")
    def counter_resolver(count, info):
        return count + 1
    
    return schema_generator.get_schema(type_def)



def example_schema():

 
    type_def = """

        interface Node {
            id: ID!
            label: String!
        }

        interface Relationship implements Node {
            id: ID!
            label: String!
            inv: ID!
            outv: ID!
        }

        type Person {
            id: ID!
            label: String!
            name: String
        }

        type Project {
            id: ID!
            label: String!
            name: String
        }
        
        type Query {
            person: Person
        }

        type Mutation {
            ok: String
        }
        
        type Subscription {
            counter: Int!
        }
    """
    from graphql import (
        GraphQLSchema,
        assert_valid_schema,
        build_ast_schema,
        parse,
    )

    schema_generator = AriadneGraphQLSchemaGenerator()
 
    @schema_generator.subscription.source("counter")
    async def counter_generator(obj, info):
        for i in range(50):
            await asyncio.sleep(1)
            yield i


    @schema_generator.subscription.field("counter")
    def counter_resolver(count, info):
        return count + 1
    

    schema_generator.query.set_field("person", lambda x, y: {
        "id":1, "label": "Hello", "name": "Hello world"})

    # schema_generator.query.field("person_by_id", )
    
    # schema_generator.query.set_field("person_by_id", lambda x, y: {
    #     "id":1, "label": "Hello", "name": "Hello world"})
    
    return schema_generator.get_schema(type_def)

