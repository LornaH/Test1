import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Store original activities for reset between tests
ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_app_state():
    """Reset global activity state before each test."""
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    yield


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)
