# Microservices - Produktionsumgebung

## Technologien

- Flask (https://flask.palletsprojects.com/en/3.0.x/)
- ApiFlask (https://apiflask.com/)
- SQLAlchemy (https://www.sqlalchemy.org/)
- mySQL (https://www.mysql.com/de/)
- Docker Compose (https://docs.docker.com/compose/)
- pyTest (https://docs.pytest.org/en/8.0.x/)
- Gunicorn (https://gunicorn.org/)

## Zweck

Dies ist eine Testapplikation für einen dockerized Flask-Server mit einer Dev und einer Prod Variante.

Es soll aufgezeigt werden was während dem Modul Microservices gelernt wurde. 

Der Source Code ist ausschliesslich für Entwicklungszwecke gedacht. Rechtlich darf der RIOT API KEY nicht ohne Erlaubnis produktiv genutzt werden.


## Funktionen

- Spieler, Teams und Turniere erstellen und verwalten
- Teams Turnieren zuordnen
- Randomized Matchups generieren

## Installation

klone dieses Repo und wechsle in das Verzeichnis mit der Datei compose.yaml

Development Env (mit Hot Reload):

```bash
docker compose up --build
```

Tests ausführen:

```bash
docker compose -f compose.test.yaml up --build
```

Produktion:

```bash
docker compose -f compose.prod.yaml up --build
```

## CI/CD

Eine Konfiguration für GitLab-CI ist im Projekt angelegt. Damit die Pipeline funktioniert müssen folgende Variablen bei den Projekt- oder Gruppen-CI Variablen gesetzt werden:

- DEPLOY_TARGET - die IP-Adresse oder der DNS-Name des Ziel-Servers
- DEPLOY_TARGET_USER - der user, mit dem wir uns auf dem target server einloggen
- SSH_PRIVATE_KEY - der private SSH-Key des Servers (auf AWS EC2 normalerweise während der Erstellung generiert)
- DB_ROOT_PASSWORD - das Root Passwort der MySQL-Datenbank
- RIOT_API_KEY - Ein Developer Key kann gratis über einenen Riot Account angefordert werden. Dieser ist 24h gültig.


## Lizenz

© 2025. This work is openly licensed via [CC BY-NC.SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).