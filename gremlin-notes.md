pipenv install git+https://github.com/invanalabs/invana-py.git@dev#egg=invana


```bash

docker run --restart always --name janusgraph-instance-1 -d -p 8182:8182 janusgraph/janusgraph
docker run --restart always --name janusgraph-test-instance-1 -d -p 8184:8182 janusgraph/janusgraph

```

```bash
docker  exec  -it janusgraph-instance-1 ./bin/gremlin.sh
:remote connect tinkerpop.server conf/remote.yaml session
:remote console
:remote config timeout none
:remote config timeout 800000
```

```bash

GraphOfTheGodsFactory.load(graph)
```

```bash
mgmt = graph.openManagement()
mgmt.printSchema()
```
