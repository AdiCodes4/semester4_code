from test import client
from test.conftest import get_auth_headers  # Assuming token is defined in conftest.py
import pytest

def test_get_tournament(client):
    headers = get_auth_headers(client, "testuser1@testmail.ch", "Test%1234")
    response = client.get("/tournament/", headers=headers)
    assert response.status_code == 200
    assert response.json[0]['name'] == 'Test Tournament'

def test_post_tournament(client):
    headers = get_auth_headers(client, "testuser1@testmail.ch", "Test%1234")
    response = client.post("/tournament/", headers=headers, json={
            'name': 'tourney2'
        })
    assert response.status_code == 201
    assert response.json['name'] == 'tourney2'

def test_change_tournament(client):
    headers = get_auth_headers(client, "testuser1@testmail.ch", "Test%1234")
    response = client.put("/tournament/1/name", headers=headers, json={'name': 'test'})
    assert response.status_code == 200
    assert response.json['name'] == 'test'

def test_delete_tournament(client):
    headers = get_auth_headers(client, "testuser1@testmail.ch", "Test%1234")
    response = client.delete("/tournament/1", headers=headers)
    assert response.status_code == 204