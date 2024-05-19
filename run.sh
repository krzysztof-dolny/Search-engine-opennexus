#!/bin/bash
export PYTHONDONTWRITEBYTECODE=1
if [ -z "$1" ]; then
    echo "No argument provided. Please use 'debug' or 'release' to run the script."
elif [ "$1" == "debug" ]; then
    python3 -m flask --app ./app run --host=0.0.0.0 --port=5000 --debug
elif [ "$1" == "release" ]; then
    python3 release.py
else
    echo "Invalid argument: $1. Please use 'debug' or 'release' to run the script."
fi