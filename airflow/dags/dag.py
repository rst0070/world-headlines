from datetime import datetime, timedelta
from airflow.decorators import dag, task, task_group
import os
import logging
from typing import List, Tuple
from custom.hooks import DBHook
from custom import operators
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

MSSQL_CONN_STR = os.getenv('MSSQL_CONN_STR')
GITHUB_REPO_CONN_STR = os.getenv('GITHUB_REPO_CONN_STR')

assert type(MSSQL_CONN_STR) is str, "Cannot read MSSQL_CONN_STR from airflow/.env"
assert type(GITHUB_REPO_CONN_STR) is str, "Cannot read GITHUB_REPO_CONN_STR from airflow/.env"

logger = logging.getLogger(__name__)

default_args = {
    'owner'         : 'rst0070',
    'retries'       : 2,
    'retry_delay'   : timedelta(minutes=2)
}
        
@dag(
    dag_id = 'world-headlines-crawler',
    default_args=default_args,
    description= 'updating db of world headlines',
    start_date = datetime(2024, 10, 14),
    schedule_interval='@hourly',
    concurrency = 5,
    max_active_runs = 1,
    catchup=False,
)
def workflow():
    
    crawl_max_num = 50
    update_gap = timedelta(minutes=20)
    
    temps_path = os.path.join(os.path.dirname(__file__), '..', 'temps')
    
    github_repo_local_path = os.path.join(temps_path, 'repo')
    db_export_path = os.path.join(github_repo_local_path, 'data')
    
    # --------------------- Get metadata
    _dbhook = DBHook(MSSQL_CONN_STR)
    metadata_list: List[dict] = _dbhook.get_metadata()
    
    # --------------------- Run task group
    task_groups = []
    for metadata in metadata_list:
        
        @task_group(group_id = f"update_{metadata['country_code']}")
        def update_headline_by_country(
            db_conn_str:str, 
            gnews_headline_url:str,
            country_code:str,
            crawl_max_num:int
            ):
            
            check_gnews_update = operators.UpdateBranchOperator(
                    task_id=f"update_branch_{country_code}",
                    next_task_id=f"update_{country_code}.crawl_gnews_{country_code}",
                    jump_task_id="pull_github_page_repo",
                    time_gap=update_gap,
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
            
            archive_old_articles = operators.ArchiveOldArticles(
                    task_id = f"archive_old_articles_{country_code}",
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
            
            check_gnews_update >> crawl_gnews >> archive_old_articles >> insert_new_articles >> delete_crawled_articles
            
        country_update = update_headline_by_country(
            db_conn_str = MSSQL_CONN_STR,
            gnews_headline_url=metadata['url'],
            country_code = metadata['country_code'],
            crawl_max_num=crawl_max_num
        )

        
        task_groups.append(country_update)
        
    # # --------------------- Pull Github repo
    # pull_repo = operators.PullGithubRepo(
    #     task_id = "pull_github_page_repo",
    #     repo_conn_str=GITHUB_REPO_CONN_STR,
    #     repo_dir_path=github_repo_local_path,
    #     trigger_rule = "none_failed"
    # )
    # # --------------------- Export DB data to the github repo
    # tasks = []
    # for metadata in metadata_list:
    #     export_db = operators.ExportDB(
    #             task_id = f"export_db_{metadata['country_code']}",
    #             db_conn_str=MSSQL_CONN_STR,
    #             country_code=metadata['country_code'],
    #             dest_dir_path=db_export_path
    #         )

    #     tasks.append(export_db)
    
    # # --------------------- Export metadata to the github repo
    # export_metadata = operators.ExportMetadata(
    #     task_id = "export_metadata_to_repo",
    #     db_conn_str=MSSQL_CONN_STR,
    #     dest_dir_path=db_export_path
    # )
    # # --------------------- Push to github
    # update_github_repo = operators.UpdateGithubRepo(
    #     task_id = "update_github_repo",
    #     repo_dir_path=github_repo_local_path
    # )
    
    
    # task_groups >> pull_repo >> tasks >> export_metadata >> update_github_repo
    
    task_groups
    
    
    
workflow()
    
    
    
    
