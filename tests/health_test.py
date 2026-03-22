import pytest
import requests 

ENDPOINT = "https://bookish-waffle-9vp65q79g7jh955v-8000.app.github.dev"

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

