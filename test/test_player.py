from test import client
from test.conftest import get_auth_headers  # Assuming token is defined in conftest.py
import pytest

def test_get_players(client):
    headers = get_auth_headers(client, "testuser1@testmail.ch", "Test%1234")
    response = client.get("/players/", headers=headers)
    assert response.status_code == 200
    assert response.json[3]['summoner_name'] == 'Atli'
    assert response.json[3]['tag'] == '2653'

def test_post_players(client):
    headers = get_auth_headers(client, "testuser1@testmail.ch", "Test%1234")
    response = client.post("/players/",headers=headers, json={
            'summoner_name': 'smiley', 'tag': '1gram', 'team_id': '1'
        })
    assert response.status_code == 201

def test_change_player(client):
    headers = get_auth_headers(client, "testuser1@testmail.ch", "Test%1234")
    response = client.put("/players/2/team", headers=headers, json={'team_id': '3'})
    assert response.status_code == 200
    assert response.json['team_id'] == 3

def test_delete_player(client):
    headers = get_auth_headers(client, "testuser1@testmail.ch", "Test%1234")
    response = client.delete("/players/2", headers=headers)
    assert response.status_code == 204


