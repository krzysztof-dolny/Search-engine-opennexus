@echo off
if not exist .env (
    echo Missing .env file
    exit /b 1
)

docker compose -f docker-compose.release.yaml up -d --build
