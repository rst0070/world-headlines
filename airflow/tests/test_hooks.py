import pytest
from hooks import DBHook, MetadataHook

# def test_dbhook(mssql_conn_str):
    
#     from sqlalchemy.engine import Engine
#     from sqlalchemy import text
    
#     hook = DBHook(mssql_conn_str)
    
#     engine = hook.get_engine()
#     assert type(engine) is Engine
    
#     with engine.begin() as conn:
#         res = conn.execute(
#             text("SELECT * FROM HEADLINE")
#         ).all()
        
#         assert len(res) != 0

def test_metadata_hook(mssql_conn_str):
    
    assert type(mssql_conn_str) is str
    
    hook = MetadataHook(db_conn_str = mssql_conn_str)
    metadata_list = hook.get_metadata()
    assert type(metadata_list) is list
    
    key_list = ['country_code', 'country_name', 'url']
    
    for metadata in metadata_list:
        assert type(metadata) is dict
        for key in metadata.keys():
            assert key in key_list 
        