import uvicorn
from invana.server.app import app

if __name__ == "__main__":
    uvicorn.run(app)
