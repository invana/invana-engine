# invana-engine

Unified graph data modelling and management toolkit served as GraphQL API.


[![Apache license](https://img.shields.io/badge/license-Apache-blue.svg)](https://github.com/invanalabs/invana-engine/blob/master/LICENSE) 
[![Build Status](https://travis-ci.org/invanalabs/invana-engine.svg?branch=develop)](https://travis-ci.org/invanalabs/invana-engine)
[![Commit Activity](https://img.shields.io/github/commit-activity/m/invanalabs/invana-engine)](https://github.com/invanalabs/invana-engine/commits)
<!-- [![codecov](https://codecov.io/gh/invanalabs/invana-engine/branch/develop/graph/badge.svg)](https://codecov.io/gh/invanalabs/invana-engine) -->


## Features 

- [ ] Vendor agnostic GraphQL API
- [ ] graph data modelling
- [ ] Interactive Search - filter and traverse through data.
- [ ] Query streaming 
- [ ] Extendable to support any graph database
<!-- - [ ] Support for large scale queries with Apache Spark -->
<!-- - [ ] graph data management system -->


## Supported Databases

| database 	    | query language 	| query     | search 	        | modelling 	|
|----------	    |----------------	|-------	|--------	        |-----------	|
| Janusgraph    | Gremlin          	| YES     	| filter/traversal  | READ          |
| Amazon Neptune| Gremlin          	| YES      	| WIP     	        |           	|
| CosmosDB      | Gremlin         	| YES      	| WIP     	        |           	|
| Datastax(DSE) | Gremlin           | YES       | WIP     	        |           	|
| Neo4j         | Cypher            | YES       |                   |               |
| ArcadeDB      | Gremlin,Cypher,SQL|           |                   |               |

**Note** Any database that supports Cypher or Gremlin can be supported extending the 
existing functionality. Checkout how to add new graph db support by extending [invana_engine/backends/base](invana_engine/backends/base/README.md)


## How to get started

### 1. with gremlin supported databases
```
# start janusgraph instance 
docker run -it -p 8182:8182 -d janusgraph/janusgraph

# start invana engine
export GRAPH_BACKEND_URL="ws://localhost:8182/gremlin"
export GRAPH_BACKEND="GremlinConnector"
uvicorn invana_engine.server.app:app --port=8200 --host=0.0.0.0 --loop=asyncio
```

### 2. with neo4j database
```
# start neo4j instance 
docker run -d -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/supersecret neo4j 


export GRAPH_BACKEND=CypherConnector
export GRAPH_BACKEND_URL="neo4j://localhost:17687"
export GRAPH_BACKEND_DATABASE_NAME=neo4j
export GRAPH_BACKEND_AUTH_USERNAME=neo4j
export GRAPH_BACKEND_AUTH_PASSWORD=supersecret
uvicorn invana_engine.server.app:app --port=8200 --host=0.0.0.0 --loop=asyncio
```

This will start invana-engine service at 8200 port. GraphQL API can be 
accessed at `http://localhost:8200/graphql`

For more `-e` options, check [invana_engine/settings.py](invana_engine/settings.py) 


## License 

Apache License 2.0
