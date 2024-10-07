from typing import List
from airflow.hooks.base import BaseHook
from airflow.utils.log.logging_mixin import LoggingMixin

from sqlalchemy.engine import Engine
from sqlalchemy import create_engine, text

class DBHook(BaseHook):
    
    def __init__(self, conn_str, *args, **kwargs):
        
        super(DBHook, self).__init__(*args, **kwargs)
        
        self.engine = create_engine(conn_str)
        
    def get_engine(self) -> Engine:
        return self.engine
    
class MetadataHook(BaseHook, LoggingMixin):
    
    def __init__(
        self,
        db_conn_str:str,
        *args, 
        **kwargs
    ):
        super(MetadataHook, self).__init__(*args, **kwargs)
        
        self.db_conn_str = db_conn_str
    
    def get_metadata(self) -> List[dict]:
        """
        Returns
        
            List[dict]: e.g. [{'country_code' : v1,'country_name' : v2, 'url' : v3}, ...]
        """
        hook = DBHook(self.db_conn_str)
        engine = hook.get_engine()
        
        with engine.begin() as conn:
            
            result = conn.execute(
                text(
                    """
                    SELECT
                        country_code,
                        country_name,
                        last_update,
                        url
                    FROM
                        HEADLINE
                    """
                )
            ).all()
            
            data = []
            for row in result:
                data.append(
                    {
                        'country_code' : row[0],
                        'country_name' : row[1],
                        'last_update'  : row[2],
                        'url'          : row[3]
                    }
                )
            
            return data