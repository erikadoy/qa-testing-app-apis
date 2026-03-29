import pytest
import requests
import uuid

ENDPOINT = "http://127.0.0.1:8000"

def new_project_payload():
    return {
        "project_name": f"TestProject-{uuid.uuid4()}",
        "team_name": "Platform Engineering",
        "status": "active",
        "templates": ["frontend-react"]
    }

def create_project(payload):
    return requests.post(f"{ENDPOINT}/api/v1/projects", json=payload)

def delete_project(project_name):
    return requests.delete(f"{ENDPOINT}/api/v1/projects/{project_name}")

def get_project(project_name):
    return requests.get(f"{ENDPOINT}/api/v1/projects/{project_name}")

def test_can_delete_project():
    # Create a project
    payload = new_project_payload()
    create_project_response = create_project(payload)
    assert create_project_response.status_code == 201

    project_name = create_project_response.json()["project_name"]

    # Delete the project
    delete_project_response = delete_project(project_name)
    assert delete_project_response.status_code == 204

    # Confirm it is gone
    get_project_response = get_project(project_name)
    assert get_project_response.status_code == 404

    print("Delete response status code:", delete_project_response.status_code)
    print("Get after delete response status code:", get_project_response.status_code)