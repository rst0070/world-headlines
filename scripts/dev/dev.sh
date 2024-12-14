#!/bin/bash
# Project root directory
set -e
cd `dirname $0`
ROOT_DIR=`pwd`/../..

# Start containers
echo "Starting Database, Airflow, and Backend..."
docker-compose -f $ROOT_DIR/scripts/dev/compose.yaml up -d #--build
echo "Containers started."

# Tail logs
mkdir -p $ROOT_DIR/scripts/dev/logs
docker-compose -f $ROOT_DIR/scripts/dev/compose.yaml logs -f airflow-webserver > $ROOT_DIR/scripts/dev/logs/airflow-webserver.log &
docker-compose -f $ROOT_DIR/scripts/dev/compose.yaml logs -f airflow-scheduler > $ROOT_DIR/scripts/dev/logs/airflow-scheduler.log &
docker-compose -f $ROOT_DIR/scripts/dev/compose.yaml logs -f airflow-triggerer > $ROOT_DIR/scripts/dev/logs/airflow-triggerer.log &
docker-compose -f $ROOT_DIR/scripts/dev/compose.yaml logs -f airflow-init > $ROOT_DIR/scripts/dev/logs/airflow-init.log &
docker-compose -f $ROOT_DIR/scripts/dev/compose.yaml logs -f airflow-cli > $ROOT_DIR/scripts/dev/logs/airflow-cli.log &
docker-compose -f $ROOT_DIR/scripts/dev/compose.yaml logs -f backend > $ROOT_DIR/scripts/dev/logs/backend.log &
docker-compose -f $ROOT_DIR/scripts/dev/compose.yaml logs -f database > $ROOT_DIR/scripts/dev/logs/database.log &

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