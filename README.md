# invana-engine

GraphQL API and Insights engine for Apache TinkerPop supported graph databases.


**Note: Under active development.** 

[![Apache license](https://img.shields.io/badge/license-Apache-blue.svg)](https://github.com/invanalabs/invana-engine/blob/master/LICENSE) 
[![Build Status](https://travis-ci.org/invanalabs/invana-engine.svg?branch=develop)](https://travis-ci.org/invanalabs/invana-engine)
[![Commit Activity](https://img.shields.io/github/commit-activity/m/invanalabs/invana-engine)](https://github.com/invanalabs/invana-engine/commits)
[![codecov](https://codecov.io/gh/invanalabs/invana-engine/branch/develop/graph/badge.svg)](https://codecov.io/gh/invanalabs/invana-engine)


## Environment variables
Following environment variables are supported and optional variables can be 
used to authenticate gremlin server connection.

- **GREMLIN_SERVER_URL**: http or ws gremlin url. ex: ws://xx.xx.xx.xx:8182/gremlin or http://xx.xx.xx.xx:8182/gremlin
- **GREMLIN_TRAVERSAL_SOURCE**(optional): defaults: 'g'
- **GREMLIN_SERVER_USERNAME**(optional): gremlin username. ex: myusername
- **GREMLIN_SERVER_PASSWORD**(optional): gremlin password. ex: mypassword
- **SERVER_PORT**(optional, available in standalone python mode only): invana engine server port ex: defaults to 8200

## Running using Docker
```shell script.
docker run -p 8200:8200 -d  -e GREMLIN_SERVER_URL=ws://xx.xx.xx.xx:8182/gremlin --name invana-engine invanalabs/invana-engine 
```

## Running using standalone python
```shell
#example usage :
pip install invana-engine
or
pip install -e git+https://github.com/invanalabs/invana-engine.git@develop#egg=invana_engine

export GREMLIN_SERVER_URL=ws://xx.xx.xx.xx:8182/gremlin
invana-engine-start # this will start invana-engine server.
```

Optional env variable in cmd line **SERVER_PORT** can be used to run the invana engine server at
port of your interest(defaults to 8200)


This will start invana-engine service at 8200 port. GraphQL API can be 
accessed at `http://localhost:8200/graphql`




## Supported Graph Databases

- [x] janusgraph 

Invana Engine uses gremlin at the core, so in theory any database that supports 
Apache TinkerPop's Gremlin 3.4.x shall work. Vertex/Edge Id resolution, needs to be fixed to 
add any new database support.

## License 

Apache License 2.0
