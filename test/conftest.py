import pytest
from test import client

@pytest.fixture
def auth_token(client):
    #Fixture to log in and return the authentication token in the correct header format.
    response = client.post("/users/login", json={'email': 'testuser1@testmail.ch', 'password': 'Test%1234'})
    token = response.json["token"]
    # Gib das Dictionary im richtigen Header-Format zurück
    return {"Authorization": f"Bearer {token}"}

def get_auth_headers(client, email, password):
    response = client.post("/users/login", json={'email': email, 'password': password})
    if response.status_code != 200:
        raise Exception("Login failed, check credentials")
    token = response.json["token"]
    return {"Authorization": f"Bearer {token}"}
