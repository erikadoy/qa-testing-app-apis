import pytest
import requests
import uuid

ENDPOINT = "http://127.0.0.1:8000"

def test_create_project():
    unique_team_name = f"TestProject-{uuid.uuid4()}" # I want to create a unique team each time, so when it runs again, it doesnt come back with a 400 because its already created.

    payload = {
        "project_name": unique_team_name,
        "team_name": "Platform Engineering",
        "status": "active",
        "templates": ["frontend-react"]
    }

    response = requests.post(f"{ENDPOINT}/api/v1/projects", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["project_name"] == unique_team_name
    assert data["team_name"] == "Platform Engineering"
    assert data["status"] == "active"
    assert data["templates"] == ["frontend-react"]
    assert "project_id" in data

    print("Calling:", f"{ENDPOINT}/api/v1/projects")