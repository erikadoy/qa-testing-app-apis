import pytest
import requests
import uuid

ENDPOINT = "http://127.0.0.1:8000"

def test_project_full_lifecycle():
    # Step 1: Create a project
    payload = {
        "project_name": f"FullLifecycleProject-{uuid.uuid4()}",
        "team_name": "Platform Engineering",
        "status": "active",
        "templates": ["frontend-react"]
    }
    create_resp = requests.post(f"{ENDPOINT}/api/v1/projects", json=payload)
    assert create_resp.status_code == 201
    project_name = create_resp.json()["project_name"]

    # Step 2: Update the project
    updates = {"status": "maintenance", "templates": ["frontend-react", "api-gateway"]}
    update_resp = requests.put(f"{ENDPOINT}/api/v1/projects/{project_name}", json=updates)
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "maintenance"
    assert len(update_resp.json()["templates"]) == 2

    # Step 3: Get the project to verify updates
    get_resp = requests.get(f"{ENDPOINT}/api/v1/projects/{project_name}")
    assert get_resp.status_code == 200
    assert get_resp.json()["status"] == "maintenance"

    # Step 4: Delete the project
    delete_resp = requests.delete(f"{ENDPOINT}/api/v1/projects/{project_name}")
    assert delete_resp.status_code == 204

    # Step 5: Confirm deletion
    confirm_resp = requests.get(f"{ENDPOINT}/api/v1/projects/{project_name}")
    assert confirm_resp.status_code == 404

    print("Confirmed deletion response status code:", confirm_resp.status_code)
    print("Confirmed deletion response JSON:", confirm_resp.json())