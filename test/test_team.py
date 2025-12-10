from test import client
from test.conftest import get_auth_headers  # Assuming token is defined in conftest.py
import pytest

def test_get_teams(client):
    headers = get_auth_headers(client, "testuser1@testmail.ch", "Test%1234")
    response = client.get("/teams/", headers=headers)
    assert response.status_code == 200
    assert response.json[3]['name'] == 'Team4'

def test_post_teams(client):
    headers = get_auth_headers(client, "testuser1@testmail.ch", "Test%1234")
    response = client.post("/teams/", headers=headers, json={
            'name': 'Team69'
        })
    assert response.status_code == 201

def test_change_team(client):
    headers = get_auth_headers(client, "testuser1@testmail.ch", "Test%1234")
    response = client.put("/teams/2/name", headers=headers, json={'name': 'test'})
    assert response.status_code == 200
    assert response.json['name'] == 'test'

def test_delete_team(client):
    headers = get_auth_headers(client, "testuser1@testmail.ch", "Test%1234")
    response = client.delete("/teams/2", headers=headers)
    assert response.status_code == 204


