from invana import InvanaGraph


def test_execute_query():
    graph = InvanaGraph("ws://localhost:8182/gremlin")
    response = graph.connector.execute_query("mgmt = graph.openManagement(); mgmt.printSchema()")
    assert response.status_code == 200
    assert response.data is not None
    graph.close_connection()
