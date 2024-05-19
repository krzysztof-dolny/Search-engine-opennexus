@echo off
if not exist .env (
    copy template.env .env
)

docker compose -f docker-compose.debug.yaml up --detach --build
