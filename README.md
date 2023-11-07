# invana-engine

Unified graph data modelling and management toolkit served as GraphQL API for graph databases.


[![Apache license](https://img.shields.io/badge/license-Apache-blue.svg)](https://github.com/invanalabs/invana-engine/blob/master/LICENSE) 
[![Build Status](https://travis-ci.org/invanalabs/invana-engine.svg?branch=develop)](https://travis-ci.org/invanalabs/invana-engine)
[![Commit Activity](https://img.shields.io/github/commit-activity/m/invanalabs/invana-engine)](https://github.com/invanalabs/invana-engine/commits)
<!-- [![codecov](https://codecov.io/gh/invanalabs/invana-engine/branch/develop/graph/badge.svg)](https://codecov.io/gh/invanalabs/invana-engine) -->


## Features 

- [ ] Unified data modelleling for Graph databases
- [ ] GraphQL API for graph databases 
- [ ] Interactive Search - filter and traverse through data.
- [ ] Support for large scale queries with Apache Spark


## Supported Databases

| database 	    | query language 	| query 	| search 	| modelling 	|
|----------	    |----------------	|-------	|--------	|-----------	|
| Janusgraph    | Gremlin          	| YES     	| WIP       | WIP          	|
| Amazon Neptune| Gremlin          	| YES      	|        	|           	|
| CosmosDB      | Gremlin         	| YES      	|        	|           	|
| Datastax(DSE) | Gremlin           | YES       |           |               |
| Neo4j         | Cypher            | WIP       |           |               |
| ArcadeDB      | Gremlin,Cypher,SQL|           |           |               |

**Note** Any database that supports Cypher or Gremlin can be supported extending the 
existing functionality. Checkout how to add new graph db support by extending [invana_engine/backends/base](invana_engine/backends/base/README.md)


## How to get started

### 1. Start a supported graph database

```
# for example; janusgraph 
docker run -it -p 8182:8182 -d janusgraph/janusgraph
```
### 2. Start Invana Engine

```
export GRAPH_BACKEND_URL="ws://localhost:8182/gremlin"

uvicorn invana_engine.server.app:app --port=8200 --host=0.0.0.0 --loop=asyncio
```

This will start invana-engine service at 8200 port. GraphQL API can be 
accessed at `http://localhost:8200/graphql`

For more `-e` options, check [invana_engine/settings.py](invana_engine/settings.py) 


## License 

Apache License 2.0
