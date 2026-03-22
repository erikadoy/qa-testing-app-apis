import pytest
import requests 

ENDPOINT = "http://127.0.0.1:8000"

def test_can_call_endpoint():
    response = requests.get(f"{ENDPOINT}/docs")
    assert response.status_code == 200

