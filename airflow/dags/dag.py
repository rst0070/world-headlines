from datetime import datetime, timedelta
from airflow.decorators import dag, task, task_group
from airflow import DAG
from airflow.models.baseoperator import chain

import os
import logging
from typing import List, Tuple

from custom.hooks import DBHook
from custom import operators
from custom import sensors

import credentials

logger = logging.getLogger(__name__)

default_args = {
    'owner'         : 'rst0070',
    'retries'       : 0,
    'retry_delay'   : timedelta(minutes=2)
}

# token: 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

@task_group
def update_headline_by_country(
    db_conn_str:str, 
    gnews_headline_url:str,
    country_code:str,
    crawl_max_num:int
    ):
    
    
    wait_gnews_update = sensors.GNewsHeadlineSensor(
            task_id=f"wait_gnews_update_{country_code}",
            db_conn_str=db_conn_str,
            gnews_url=gnews_headline_url,
            country_code=country_code
        )
    
    crawl_gnews = operators.CrawlHeadline(
            task_id = f"crawl_gnews_{country_code}",
            db_conn_str=db_conn_str,
            gnews_url=gnews_headline_url,
            country_code=country_code,
            crawl_max_num=crawl_max_num,
            crawl_timeout_sec=5.0    
        )
    
    delete_old_articles = operators.DeleteOldArticles(
            task_id = f"delete_old_articles_{country_code}",
            db_conn_str=db_conn_str,
            country_code=country_code 
        )
    
    insert_new_articles = operators.InsertNewArticles(
            task_id = f"insert_new_articles_{country_code}",
            db_conn_str=db_conn_str,
            country_code=country_code 
        )

    delete_crawled_articles = operators.DeleteCrawledArticles(
            task_id = f"delete_crawled_articles_{country_code}",
            db_conn_str=db_conn_str,
            country_code=country_code 
        )
    
    chain(
        wait_gnews_update,
        crawl_gnews,
        delete_old_articles,
        insert_new_articles,
        delete_crawled_articles
    )


        
@dag(
    dag_id = 'world-headline-workflow',
    default_args=default_args,
    description= 'updating db of world headlines',
    start_date = datetime.now(),
    schedule_interval='@daily'
)
def workflow():
    
    crawl_max_num = 50
    
    conn_str = credentials.MSSQL_CONN_STR
    temps_path = os.path.join(os.path.dirname(__file__), '..', 'temps')
    
    
    github_repo_conn_str = credentials.GITHUB_REPO_CONN_STR
    github_repo_local_path = os.path.join(temps_path, 'repo')
    db_export_path = os.path.join(github_repo_local_path, 'data')
    
    # --------------------- Get metadata
    _dbhook = DBHook(conn_str)
    metadata_list: List[dict] = _dbhook.get_metadata()
    
    # --------------------- Run task group
    task_groups = []
    for metadata in metadata_list:
        country_update = update_headline_by_country(
            db_conn_str = conn_str,
            gnews_headline_url=metadata['url'],
            country_code = metadata['country_code'],
            crawl_max_num=crawl_max_num
        )
        
        task_groups.append(country_update)
        
    # --------------------- Pull Github repo
    pull_repo = operators.PullGithubRepo(
        task_id = "pull_github_page_repo",
        repo_conn_str=github_repo_conn_str,
        repo_dir_path=github_repo_local_path
    )
    # --------------------- Export DB data to the github repo
    tasks = []
    for metadata in metadata_list:
        export_db = operators.ExportDB(
                task_id = f"export_db_{metadata['country_code']}",
                db_conn_str=conn_str,
                country_code=metadata['country_code'],
                dest_dir_path=db_export_path
            )

        tasks.append(export_db)
    
    # --------------------- Export metadata to the github repo
    export_metadata = operators.ExportMetadata(
        task_id = "export_metadata_to_repo",
        db_conn_str=conn_str,
        dest_dir_path=db_export_path
    )
    # --------------------- Push to github
    update_github_repo = operators.UpdateGithubRepo(
        task_id = "update_github_repo",
        repo_dir_path=github_repo_local_path
    )
    
    chain(
        task_groups,
        pull_repo,
        tasks,
        export_metadata,
        update_github_repo
    )
    
    
    
workflow()
    
    
    
    
