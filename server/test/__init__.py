import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..src.main import taskpool_app


@pytest.fixture
def app() -> FastAPI:
    taskpool_app.dependency_overrides = {}

    return taskpool_app


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)
