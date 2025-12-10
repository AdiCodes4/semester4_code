from test import client
from test.conftest import get_auth_headers  # Assuming token is defined in conftest.py

# simple test to check if test framework is working

def test_root(client):
    response = client.get("/")
    assert response.status_code == 302 # Redirect to ui