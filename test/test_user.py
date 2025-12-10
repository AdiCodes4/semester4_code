from test import client
import pytest

def test_login_user(client):
    response = client.post("/users/login", json={
        "email": "testuser1@testmail.ch",
        "password": "Test%1234"
    })
    assert response.status_code == 200
    assert "token" in response.json

def test_get_users(client):
    # Login beim richtigen Endpoint
    login_response = client.post("/users/login", json={
        "email": "testuser1@testmail.ch",
        "password": "Test%1234"
    })
    assert login_response.status_code == 200
    token = login_response.json["token"]

    # Authentifizierter Request an /users/
    response = client.get("/users/", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    users = response.json

    assert isinstance(users, list)
    assert any(user["email"] == "testuser1@testmail.ch" for user in users)

def test_create_user(client):
    response = client.post("/users/", json={
        "name": "testuser5",
        "email": "testuser5@testmail.ch",
        "password": "Test%1234"
    })
    assert response.status_code == 201
    assert response.json["name"] == "testuser5"


