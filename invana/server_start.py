import uvicorn
from invana.server.app import app
import logging

logging.basicConfig(level="DEBUG")


def server_start():
    uvicorn.run(app, host="0.0.0.0")


if __name__ == "__main__":
    server_start()
