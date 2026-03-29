import pytest
import requests
import uuid

ENDPOINT = "http://127.0.0.1:8000"

def test_create_project_invalid_team():
    payload = {
        "project_name": f"InvalidTeamProject-{uuid.uuid4()}",
        "team_name": "NonExistentTeam",  # Invalid team
        "status": "active",
        "templates": ["frontend-react"]
    }
    response = requests.post(f"{ENDPOINT}/api/v1/projects", json=payload)
    assert response.status_code == 400
    assert "Invalid team name" in response.text

def test_update_project_invalid_template():
    # First, create a valid project
    payload = {
        "project_name": f"TestProject-{uuid.uuid4()}",
        "team_name": "Platform Engineering",
        "status": "active",
        "templates": ["frontend-react"]
    }
    create_resp = requests.post(f"{ENDPOINT}/api/v1/projects", json=payload)
    assert create_resp.status_code == 201

    project_name = create_resp.json()["project_name"]

    # Try updating with an invalid template
    updates = {"templates": ["non-existent-template"]}
    update_resp = requests.put(f"{ENDPOINT}/api/v1/projects/{project_name}", json=updates)
    assert update_resp.status_code == 400
    assert "Invalid template type" in update_resp.text

    print("Response status code:", update_resp.status_code)
    print("Response JSON:", update_resp.json())