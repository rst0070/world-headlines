#!/bin/bash
# Project root directory
set -e
cd `dirname $0`
ROOT_DIR=`pwd`/../..

# Down existing containers
echo "Cleaning existing containers..."
docker compose -f $ROOT_DIR/scripts/dev/compose.yaml down --volumes
echo "Cleaning containers done."

# Load environment variables from .env file
# This wil automatically set env vars for frontend (other containers use build)
env_path=$ROOT_DIR/scripts/dev/.env
if [ -f $env_path ]; then
  export $(grep -v '^#' $env_path | xargs)
fi

# Start containers
echo "Starting Database, Airflow, and Backend..."
docker compose -f $ROOT_DIR/scripts/dev/compose.yaml up -d --build
echo "Containers started."

# Tail logs
mkdir -p $ROOT_DIR/scripts/dev/logs
docker compose -f $ROOT_DIR/scripts/dev/compose.yaml logs -f airflow-webserver > $ROOT_DIR/scripts/dev/logs/airflow-webserver.log &
docker compose -f $ROOT_DIR/scripts/dev/compose.yaml logs -f airflow-scheduler > $ROOT_DIR/scripts/dev/logs/airflow-scheduler.log &
docker compose -f $ROOT_DIR/scripts/dev/compose.yaml logs -f airflow-triggerer > $ROOT_DIR/scripts/dev/logs/airflow-triggerer.log &
docker compose -f $ROOT_DIR/scripts/dev/compose.yaml logs -f airflow-init > $ROOT_DIR/scripts/dev/logs/airflow-init.log &
docker compose -f $ROOT_DIR/scripts/dev/compose.yaml logs -f airflow-cli > $ROOT_DIR/scripts/dev/logs/airflow-cli.log &
docker compose -f $ROOT_DIR/scripts/dev/compose.yaml logs -f backend > $ROOT_DIR/scripts/dev/logs/backend.log &
docker compose -f $ROOT_DIR/scripts/dev/compose.yaml logs -f database > $ROOT_DIR/scripts/dev/logs/database.log &

# frontend
echo "Starting Frontend..."
cd $ROOT_DIR/frontend_web
npm install 2>&1 > /dev/null
npm run dev 2>&1 > $ROOT_DIR/scripts/dev/logs/frontend_web.log &
echo "Frontend started."

# print logs
tail -f $ROOT_DIR/scripts/dev/logs/backend.log $ROOT_DIR/scripts/dev/logs/database.log $ROOT_DIR/scripts/dev/logs/frontend_web.log 

# Sleep forever
while true; do
  sleep 1
done