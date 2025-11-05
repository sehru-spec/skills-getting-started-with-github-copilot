import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Soccer Team" in data
    assert "Basketball Club" in data


def test_signup_for_activity_success():
    email = "newstudent@mergington.edu"
    activity = "Soccer Team"
    # Ensure not already signed up
    client.get("/activities")  # warm up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Check participant added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_for_activity_already_signed_up():
    email = "liam@mergington.edu"
    activity = "Soccer Team"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_nonexistent_activity():
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
