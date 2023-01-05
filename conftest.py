import pytest
import os


@pytest.fixture(scope="function")
def gremlin_url() -> str:
    return os.environ.get("GREMLIN_SERVER_URL", "ws://megamind.local:8182/gremlin")
