import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data


def test_signup_for_activity_success():
    email = "newstudent@mergington.edu"
    activity = "Basketball"
    # Remove if already present
    if email in client.get("/activities").json()[activity]["participants"]:
        client.delete(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    # Clean up
    client.delete(f"/activities/{activity}/unregister?email={email}")


def test_signup_for_activity_duplicate():
    email = "alex@mergington.edu"
    activity = "Basketball"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_participant():
    email = "tempuser@mergington.edu"
    activity = "Basketball"
    # Register first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert "removed" in response.json()["message"]
    # Try to remove again
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
