import uvicorn
from invana_engine.server.app import app
import logging
from invana_engine.settings import server_port, shall_debug

if shall_debug is False:
    logging.getLogger('asyncio').setLevel(logging.ERROR)
    logging.getLogger('uvicorn').setLevel(logging.ERROR)
else:
    logging.basicConfig(level="DEBUG")


def server_start():
    uvicorn.run(app, host="0.0.0.0", port=int(server_port))


if __name__ == "__main__":
    server_start()
