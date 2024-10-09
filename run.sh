cd airflow
sudo docker compose down
sudo docker build -t world-headlines-airflow .
sudo docker compose up