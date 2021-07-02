

CLIENT_RAW_QUERIES = {
    "create_query":  "g.addV('Person').property('name', 'Ravi').next()",
    "list_query": "g.V().valueMap(true).limit(4).toList()"
}
