#!/bin/bash

echo "Cloning traffic-db-storage branch..."
git clone -b traffic-db-storage https://github.com/ShawnN24/Github-Traffic-API.git cloned-repo

echo "Starting the server..."
uvicorn app.main:app --host 0.0.0.0 --port 10000