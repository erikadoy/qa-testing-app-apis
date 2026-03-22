import pytest
import requests

ENDPOINT = "https://bookish-waffle-9vp65q79g7jh955v-8000.app.github.dev"

def test_can_get_all_projects():
    response = requests.get(f"{ENDPOINT}/api/v1/projects")
    assert response.status_code == 200

def test_can_get_all_teams():
    response = requests.get(f"{ENDPOINT}/api/v1/teams")
    assert response.status_code == 200

def test_can_get_stats():
    response = requests.get(f"{ENDPOINT}/api/v1/stats")
    assert response.status_code == 200

def test_can_get_project_by_name():
    response = requests.get(f"{ENDPOINT}/api/v1/projects")
    data = response.json()

    first_project = data["projects"][0]["project_name"]

    response = requests.get(f"{ENDPOINT}/api/v1/projects/{first_project}")
    assert response.status_code == 200

def test_can_get_teams_projects():
    response = requests.get(f"{ENDPOINT}/api/v1/teams")
    data = response.json()

    team_name = data["teams"][0]["team_name"]

    response = requests.get(f"{ENDPOINT}/api/v1/teams/{team_name}/projects")
    assert response.status_code == 200

def test_can_get_template_type():
    response = requests.get(f"{ENDPOINT}/api/v1/projects")
    data = response.json()

    template_type = data["projects"][0]["templates"][0]
    
    response = requests.get(f"{ENDPOINT}/api/v1/templates/{template_type}/projects")
    assert response.status_code == 200