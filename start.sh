#!/bin/bash

echo "Fetching traffic.db from traffic-db-storage branch..."
git fetch origin traffic-db-storage
git checkout origin/traffic-db-storage -- traffic.db

echo "Starting the server..."
# Replace this with your actual server start command, e.g.:
uvicorn app.main:app --host 0.0.0.0 --port 10000