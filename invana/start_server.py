import uvicorn
from invana.server.app import app
import logging

logging.basicConfig(level="DEBUG")
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
