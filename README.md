# invana-engine

GraphQL API for Apache TinkerPop supported graph databases.

**Note: Under active development.** 

[![Apache license](https://img.shields.io/badge/license-Apache-blue.svg)](https://github.com/invanalabs/invana-engine/blob/master/LICENSE) 
[![Build Status](https://travis-ci.org/invanalabs/invana-engine.svg?branch=develop)](https://travis-ci.org/invanalabs/invana-engine)
[![Commit Activity](https://img.shields.io/github/commit-activity/m/invanalabs/invana-engine)](https://github.com/invanalabs/invana-engine/commits)
[![codecov](https://codecov.io/gh/invanalabs/invana-engine/branch/develop/graph/badge.svg)](https://codecov.io/gh/invanalabs/invana-engine)

## How to run using docker

```shell script.
docker run -p 5000:5000 -d --name invana-engine invanalabs/invana-engine \
 -e GREMLIN_SERVER_URL=ws://localhost:8182/gremlin
```

This will start invana-engine service at 5000 port. GraphQL API can be 
accessed at `http://localhost:5000/graphql`

## Supported Graph Databases

[x] janusgraph 

Invana Engine uses gremlin at the core, so in theory any database that supports 
Apache TinkerPop's Gremlin 3.4.x shall work. Id resolution, needs to be fixed to 
add any new database support.

## License 

Apache License 2.0
