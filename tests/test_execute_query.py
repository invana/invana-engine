from invana_engine.invana import InvanaGraph


class TestConnection:
 
    def test_execute_query(self, gremlin_url: str):
        graph = InvanaGraph(gremlin_url)
        response = graph.connector.execute_query("g.V().limit(1).elementMap().toList()")
        assert response.status_code == 200
        assert response.data is not None
        graph.close_connection()
