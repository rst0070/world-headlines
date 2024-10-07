from airflow.sensors.base import BaseSensorOperator
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.context import Context

from custom.hooks import DBHook
from sqlalchemy import text
from sqlalchemy.engine import Engine

import requests
import xml.etree.ElementTree as ET

import datetime
from custom import scripts

class GNewsHeadlineSensor(BaseSensorOperator, LoggingMixin):
    
    def __init__(
        self, 
        task_id,
        db_conn_str:str, 
        gnews_url:str,
        country_code:str,
        *args,
        **kwargs
        ):
        
        super(GNewsHeadlineSensor, self).__init__(task_id = task_id, *args, **kwargs)


        self.db_conn_str = db_conn_str
        self.gnews_url = gnews_url
        self.hook: DBHook | None = None
        self.country_code = country_code
        
        
    def poke(self, context: Context) -> bool:
        """
        1. get db hook if not initiated
        2. check db update and gnews update
        3. check if gnews_update is later then db_update
        """
        if self.hook is None:
            self.hook = DBHook(self.db_conn_str)
            
        db_update = self._get_last_update_of_db()
        gnews_update = self._get_last_update_of_gnews()
        
        if db_update is None:
            return True
        
        return db_update < gnews_update
    
    def _get_last_update_of_gnews(self) -> datetime.datetime:
            
        rss_req = requests.get(self.gnews_url)
        xml_root = ET.fromstring(rss_req.text)
        
        last_update_str = xml_root.find('channel').find('lastBuildDate').text
        assert type(last_update_str) is str
        
        last_update = scripts.gnews_gmt_str_to_datetime(last_update_str)
        
        self.log.info(f"last_update of GNews: {last_update}")
        return last_update
    
    def _get_last_update_of_db(self) -> datetime.datetime | None:
        
        engine: Engine = self.hook.get_engine()
        
        with engine.begin() as conn:
            
            result = conn.execute(
                text(f"SELECT last_update FROM HEADLINE WHERE country_code = '{self.country_code}'")
            )
            
            datetime2 = result.all()[0][0]
            
            self.log.info(f"last update of DB: {datetime2}")
            if datetime2 is None:
                return None
            
            
            if type(datetime2) is datetime.datetime:
                return datetime2
            else:
                return scripts.mssql_datetime2_to_datetime(datetime2) 
            
