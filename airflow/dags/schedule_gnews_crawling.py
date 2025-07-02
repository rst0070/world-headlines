from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

default_args = {
    'owner': 'Wonbin Kim',
    'start_date': datetime(2025, 6, 3),
    'schedule_interval': '@hourly',
}

with DAG(
    dag_id = 'schedule_gnews_crawling',
    default_args = default_args,
    description = 'schedule gnews crawling',
    schedule_interval = '@hourly',
    catchup=False,
) as dag:
    
    variables = {
        # "ENV": "{{var.value.ENV}}", 
        # "LOKI_URL": "{{ var.value.LOKI_URL }}",
        "INFISICAL_HOST": "{{ var.value.INFISICAL_HOST }}",
        "INFISICAL_TOKEN": "{{ var.value.INFISICAL_TOKEN }}",
        "INFISICAL_PROJECT_ID": "{{ var.value.INFISICAL_PROJECT_ID }}",
        "INFISICAL_ENVIRONMENT": "prod"
    }

    task = KubernetesPodOperator(
        task_id = 'gnews_crawling',
        name = 'gnews_crawling',
        # namespace = 'workflow-jobs',
        env_vars = variables,
        kubernetes_conn_id = 'rst0070-k3s-workflow-jobs',
        image = 'harbor.rst0070.com/world-headlines/gnews-crawling:latest',
        image_pull_policy = 'Always',
        is_delete_operator_pod = False,
        get_logs = True,
        dag = dag,
    )