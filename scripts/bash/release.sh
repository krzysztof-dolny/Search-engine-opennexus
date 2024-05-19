#!/bin/bash
if [ ! -f .env ]; then
    echo "Missing .env file"
fi
docker compose -f docker-compose.release.yaml up -d --build