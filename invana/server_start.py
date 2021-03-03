import uvicorn
from invana.server.app import app
import logging
from settings import server_port, shall_debug

if shall_debug is False:
    logging.getLogger('asyncio').setLevel(logging.ERROR)
    logging.getLogger('uvicorn').setLevel(logging.ERROR)

logging.basicConfig(level="DEBUG")


def server_start():
    uvicorn.run(app, host="0.0.0.0", port=server_port)


if __name__ == "__main__":
    server_start()
