#!/bin/bash

echo "Downloading traffic.db from GitHub..."
curl -o traffic.db https://raw.githubusercontent.com/${GITHUB_USERNAME}/Github-Traffic-API/traffic-db-storage/traffic.db

echo "Starting the server..."
uvicorn app.main:app --host 0.0.0.0 --port 10000