import pytest
from sensors import GNewsHeadlineSensor
from hooks import MetadataHook
import random

@pytest.fixture
def metadata_hook(mssql_conn_str):
    return MetadataHook(db_conn_str=mssql_conn_str)
    
    
def test_gnews_headline_sensor(mssql_conn_str, metadata_hook,test_dag):
    
    for metadata in metadata_hook.get_metadata():
        
        sensor = GNewsHeadlineSensor(
            task_id = f"gnews_headline_sensor_{metadata['country_code']}",
            db_conn_str = mssql_conn_str,
            gnews_url = metadata['url'],
            country_code = metadata['country_code'],
            dag = test_dag,
        )
        
        pytest.helpers.run_task(task = sensor, dag = test_dag)
    
    