import uvicorn
from invana.server.app import app
import logging

logging.basicConfig(level="DEBUG")


def start_server():
    uvicorn.run(app, host="0.0.0.0")


if __name__ == "__main__":
    start_server()
