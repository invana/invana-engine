# References 


https://medium.com/enharmonic/evolving-data-models-with-janusgraph-d0ecf6d3fda3

```bash
docker run -d -it -p 8182:8182 --name janusgraph janusgraph/janusgraph         
export GREMLIN_SERVER_URL=ws://megamind-ws:8182/gremlin
uvicorn invana_engine.server.app:app  --loop=asyncio --reload --port 8200
```
