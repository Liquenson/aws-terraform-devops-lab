import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_index_returns_json(client):
    response = client.get("/")
    data = response.get_json()
    assert data["app"] == "devops-lab-webapp"
    assert data["status"] == "ok"
    assert "version" in data
    assert "environment" in data


def test_index_only_get_allowed(client):
    response = client.post("/")
    assert response.status_code == 405


def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_healthy(client):
    response = client.get("/health")
    data = response.get_json()
    assert data["status"] == "healthy"


def test_ready_returns_200(client):
    response = client.get("/ready")
    assert response.status_code == 200


def test_ready_returns_ready(client):
    response = client.get("/ready")
    data = response.get_json()
    assert data["status"] == "ready"


def test_index_with_env_vars(client, monkeypatch):
    monkeypatch.setenv("APP_VERSION", "2.0.0")
    monkeypatch.setenv("AWS_REGION", "eu-west-1")
    response = client.get("/")
    data = response.get_json()
    assert data["version"] == "2.0.0"
    assert data["environment"] == "eu-west-1"
