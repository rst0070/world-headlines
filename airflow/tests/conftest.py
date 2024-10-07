from typing import Generator

import datetime
import pytest
from airflow import DAG
from collections import namedtuple
import pytest
from pytest_docker_tools import container, fetch

import sys
import os

from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../plugins')))

pytest_plugins = ["helpers_namespace"]

@pytest.fixture
def test_dag():
    return DAG(
        "test_dag",
        default_args={'owner': 'airflow', 'start_date': datetime.datetime(2024, 10, 6)},
        schedule_interval=datetime.timedelta(days=1),
    )


@pytest.helpers.register
def run_task(task, dag):
    dag.clear()
    task.run(
        start_date=dag.default_args["start_date"],
        end_date=dag.default_args["start_date"],
    )
    

@pytest.fixture
def mssql_conn_str() -> Generator[str, None, None]:
    """
    It sets up database and tear down it after test process.

    Yields:
        Generator[str]: connection string to mssql DB
    """
    conn_str_admin_test = "mssql+pyodbc://sa:WonbinsOldLaptopMssql99!@1.240.103.57:3021/world_headlines_test?driver=ODBC+Driver+17+for+SQL+Server"
    conn_str_updater = "mssql+pyodbc://wh_updater:WorldHeadlinesUpdater99!@1.240.103.57:3021/world_headlines_test?driver=ODBC+Driver+17+for+SQL+Server"
    
    # ------------------ set up process
    engine = create_engine(conn_str_admin_test)
    if not database_exists(engine.url):
        create_database(engine.url)
        
    with open(os.path.join(os.path.dirname(__file__), 'mssql_set_up.sql'), 'r') as file:
        with engine.begin() as conn:
            query = text(file.read())
            conn.execute(query)

    # ------------------ pass the connection string
    yield conn_str_updater  
    
    # ------------------ tear down process
    with open(os.path.join(os.path.dirname(__file__), 'mssql_tear_down.sql'), 'r') as file:
        with engine.begin() as conn:
        
            query = text(file.read())
            conn.execute(query)

@pytest.fixture
def metadata():
    return [
        {
            "country_code":"br",
            "country_name":"Brasil",
            "url":"https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYQjBMVUpTR2dKQ1VpZ0FQAQ?ceid=BR:pt-419&oc=3&hl=pt-BR&gl=BR"
        },
        {
            "country_code":"us",
            "country_name":"United States",
            "url":"https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pWVXlnQVAB?ceid=US:en&oc=3"
        },
        {
            "country_code":"tw",
            "country_name":"Taiwan",
            "url":"https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVlJYR2dKVVZ5Z0FQAQ?ceid=TW:zh-Hant&oc=3"
        },
        {
            "country_code":"ru",
            "country_name":"Russia",
            "url":"https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FuSjFHZ0pTVlNnQVAB?ceid=RU:ru&oc=3"
        },
        {
            "country_code":"kr",
            "country_name":"Korea",
            "url":"https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtdHZHZ0pMVWlnQVAB?ceid=KR:ko&oc=3"
        },
        {
            "country_code":"jp",
            "country_name":"Japan",
            "url":"https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtcGhHZ0pLVUNnQVAB?ceid=JP:ja&oc=3"
        },
        {
            "country_code":"in",
            "country_name":"India",
            "url":"https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JXVnVMVWRDR2dKSlRpZ0FQAQ?ceid=IN:en&oc=3"
        },
        {
            "country_code":"gb",
            "country_name":"United Kingdom",
            "url":"https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JXVnVMVWRDR2dKSFFpZ0FQAQ?ceid=GB:en&oc=3"
        },
        {
            "country_code":"fr",
            "country_name":"Franch",
            "url":"https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtWnlHZ0pHVWlnQVAB?ceid=FR:fr&oc=3"
        },
        {
            "country_code":"de",
            "country_name":"German",
            "url":"https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtUmxHZ0pFUlNnQVAB?ceid=DE:de&oc=3"
        },
        {
            "country_code":"cn",
            "country_name":"China",
            "url":"https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVU5PR2dKRFRpZ0FQAQ?ceid=CN:zh-Hans&oc=3"
        },
    ]
		
		
		
		
		
		
		
		
		
		