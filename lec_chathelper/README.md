# ENDPOINT

1. GET /credentials?url=token
The token will be parsed to get username, then used this to find and send the token back for server.

## How to test

1. Roll up the test database and then test:
```console
docker compose up -d
python manage.py test
```