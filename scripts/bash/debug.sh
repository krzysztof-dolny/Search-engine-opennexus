#!/bin/bash
if [ ! -f .env ]; then
    cp template.env .env
fi
docker compose -f docker-compose.debug.yaml up --detach --build