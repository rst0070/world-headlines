cd airflow
docker compose down
docker build -t world-headlines-airflow .
docker compose up
pause