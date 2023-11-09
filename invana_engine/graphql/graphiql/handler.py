from typing import (
    Any,
    Callable,
    Dict,

)

from starlette.requests import Request
from starlette.responses import HTMLResponse, Response


def generate_html(server_uri):
   return f"""
   <!doctype html>
   <html lang="en">
      <head>
         <meta charset="utf-8"/>
         <meta name="viewport" content="width=device-width,initial-scale=1"/>
         <meta name="theme-color" content="#000000"/>
         <meta name="description" content="Opensource GraphQL API for modelling and querying graph data "/>
         <link rel="manifest" href="/manifest.json"/>
         <title>Invana Engine</title>
         <script defer="defer" src="/static/js/main.4cb84a9b.js"></script>
         <link href="/static/css/main.28998c47.css" rel="stylesheet">
      </head>
      <body>
         <noscript>You need to enable JavaScript to run this app.</noscript>
         <div id="root"></div>
      </body>
      <script>
         localStorage.setItem("INVANA_ENGINE_URL", "{server_uri}graph/");
      </script>
   </html>
   """


def make_graphiql_handler() -> Callable[[Request], Response]:
    def handler(request: Request) -> Response:
        return HTMLResponse(generate_html(request.base_url._url))

    return handler
