from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from invana_engine.graph import InvanaGraph


class InvanaApp(Starlette):

    graph: InvanaGraph

    def __init__(self, *args, graph=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.graph = graph
