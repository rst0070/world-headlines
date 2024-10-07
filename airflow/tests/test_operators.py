import operators
import pytest

def test_crawl_headline(mssql_conn_str, metadata, test_dag):
    
    tasks = []
    
    for m in metadata:
        task = operators.CrawlHeadline(
            db_conn_str = mssql_conn_str,
            gnews_url=m["url"],
            country_code = m['country_code'],
            crawl_max_num=5,
            task_id = f"crawl_headline_{m['country_code']}",
            dag = test_dag
        )
        
        pytest.helpers.run_task(task=task, dag=test_dag)