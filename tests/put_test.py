import pytest
import requests
import uuid

ENDPOINT = "http://127.0.0.1:8000"

def test_can_update_project():
    payload = {
        "project_name": f"TestProject-{uuid.uuid4()}",
        "team_name": "Platform Engineering",
        "status": "active",
        "templates": ["frontend-react"]
    }
    # Create
    create_response = requests.post(f"{ENDPOINT}/api/v1/projects", json=payload)
    assert create_response.status_code == 201
    project_name = create_response.json()["project_name"]

    # Update
    updates = {"team_name": "Cloud Infrastructure", "status": "maintenance", "templates": ["api-gateway"]}
    update_response = requests.put(f"{ENDPOINT}/api/v1/projects/{project_name}", json=updates)
    assert update_response.status_code == 200

    # Verify
    get_response = requests.get(f"{ENDPOINT}/api/v1/projects/{project_name}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["team_name"] == updates["team_name"]

    print("Update response status code:", update_response.status_code)
    print("Update response JSON:", update_response.json())