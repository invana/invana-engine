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
| Janusgraph    | Gremlin          	| YES     	| YES       | WIP          	|
| Amazon Neptune| Gremlin          	| YES      	|        	|           	|
| CosmosDB      | Gremlin         	| YES      	|        	|           	|
| Datastax(DSE) | Gremlin           | YES       |           |               |
| Neo4j         | Cypher            |           |           |               |

**Note** Any database that supports Cypher or Gremlin can be supported extending 
the 

## How to get started

### 1. Start a supported graph database

```
# for example; janusgraph 
docker run -it -p 8182:8182 -d janusgraph/janusgraph
```
### 2. Start Invana Engine

```
docker run -p 8200:8200 -d -e GREMLIN_SERVER_URL=ws://xx.xx.xx.xx:8182/gremlin --name invana-engine invanalabs/invana-engine 
```

This will start invana-engine service at 8200 port. GraphQL API can be 
accessed at `http://localhost:8200/graphql`

For more `-e` options, check [invana_engine/settings.py](invana_engine/settings.py) 


## License 

Apache License 2.0
