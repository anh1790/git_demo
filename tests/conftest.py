"""
Pytest configuration and global fixtures for AirSense AI Test Suite.
"""

import sys
import json
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.lifespan import state

def run_coroutine(coro):
    """
    Direct synchronous coroutine executor for non-blocking FastAPI route handlers.
    Avoids AnyIO thread deadlock issues on Windows / Python 3.14.
    """
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value

@pytest.fixture(scope="session")
def app_state():
    """Session-scoped fixture providing warm, pre-loaded AI models and geospatial state."""
    state.ensure_started()
    return state

@pytest.fixture(scope="session")
def test_fixtures():
    """Loads static fixture data including hashes and payloads."""
    fixtures_file = BASE_DIR / "tests" / "fixtures" / "test_payloads.json"
    with open(fixtures_file, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture(scope="session")
def index_html_content():
    """Loads the main index.html for frontend DOM inspection."""
    html_file = BASE_DIR / "index.html"
    with open(html_file, "r", encoding="utf-8") as f:
        return f.read()

@pytest.fixture(scope="session")
def stations_js_content():
    """Loads stations_data.js for client data verification."""
    js_file = BASE_DIR / "js" / "stations_data.js"
    with open(js_file, "r", encoding="utf-8") as f:
        return f.read()
