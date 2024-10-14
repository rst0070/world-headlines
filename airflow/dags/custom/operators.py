"""
    - crawl headline into `CRAWLED_ARTICLES` 
        - (need: gnews_url, identity of country)
    - delete old articles in `HEADLINE_ARTICLES` 
        - (need: identity of country)
    - insert new articles into `HEADLINE_ARTICLES` 
        - (need: identity of country)
    - delete crawled articles
    
"""
from airflow.models import BaseOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.log.logging_mixin import LoggingMixin

from custom.hooks import DBHook, CrawlHeadlineHook
from sqlalchemy import text
from sqlalchemy.engine import Engine

import requests
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from custom import scripts
from typing import List,Tuple

import datetime
import os
import subprocess
import json


class UpdateBranchOperator(BranchPythonOperator, LoggingMixin):
    
    def __init__(
        self,
        task_id,
        next_task_id,
        jump_task_id,
        time_gap:datetime.timedelta,
        db_conn_str:str, 
        gnews_url:str,
        country_code:str,
        *args,
        **kwargs
        ):
        
        
        super(UpdateBranchOperator, self).__init__(
            task_id = task_id, 
            python_callable = self._branch,
            *args,
            **kwargs)

        self.db_conn_str = db_conn_str
        self.gnews_url = gnews_url
        self.country_code = country_code
        
        self.next_task_id = next_task_id
        self.jump_task_id = jump_task_id
        
        self.time_gap = time_gap
        
    def _branch(self):
        
        hook = DBHook(self.db_conn_str)
        
        db_update = self._get_last_update_of_db(hook)
        gnews_update = self._get_last_update_of_gnews()
        
        if db_update is None:
            return self.next_task_id
        
        if (db_update + self.time_gap) < gnews_update:
            return [self.next_task_id]
        
        return [self.jump_task_id]

    def _get_last_update_of_gnews(self) -> datetime.datetime:
            
        rss_req = requests.get(self.gnews_url)
        xml_root = ET.fromstring(rss_req.text)
        
        last_update_str = xml_root.find('channel').find('lastBuildDate').text
        assert type(last_update_str) is str
        
        last_update = scripts.gnews_gmt_str_to_datetime(last_update_str)
        
        self.log.info(f"last_update of GNews: {last_update}")
        return last_update
    
    def _get_last_update_of_db(self, hook) -> datetime.datetime | None:
        
        engine: Engine = hook.get_engine()
        
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

class CrawlHeadline(BaseOperator, LoggingMixin):
    
    def __init__(
        self,
        db_conn_str:str,
        gnews_url:str,
        country_code:str,
        crawl_max_num:int,
        crawl_timeout_sec:float = 5.0,
        *args,
        **kwargs):
        """
        THIS IS ACTION PER COUNTRY !!!

        Args:
            db_conn_str (str): _description_
            gnews_url (str): _description_
            country_code (str): _description_
            crawl_max_num (int): _description_
            crawl_timeout_sec (float, optional): _description_. Defaults to 5.0.
        """
        
        super(CrawlHeadline, self).__init__(*args, **kwargs)
        
        self.db_conn_str = db_conn_str
        self.gnews_url = gnews_url
        self.country_code = country_code
        self.crawl_max_num = crawl_max_num
        self.crawl_timeout_sec:float = crawl_timeout_sec
        
    def execute(self, context):
        
        crawl_hook = CrawlHeadlineHook(
                        self.gnews_url,
                        self.country_code,
                        self.crawl_max_num,
                        self.crawl_timeout_sec
                    )
        
        articles, last_update = crawl_hook.crawl()
        articles = [
            {
                'country_code' : article.country_code,
                'url' : article.url,
                'title' : article.title,
                'description' : article.description,
                'image_url' : article.image_url,
                'publish_date' : str(article.publish_date),
                'source' : article.source
                
            } for article in articles
        ]
    
        db_hook = DBHook(self.db_conn_str)
        engine = db_hook.get_engine()
        
        with engine.begin() as conn:
            
            conn.execute(
                text(
                """
                IF NOT EXISTS (
                    SELECT 1
                    FROM CRAWLED_ARTICLES
                    WHERE
                        country_code = :country_code
                        and url = :url
                )
                BEGIN
                    INSERT INTO CRAWLED_ARTICLES(country_code,url,title,description,image_url,publish_date,source)
                    VALUES(:country_code,:url,:title,:description,:image_url,:publish_date,:source)
                END
                """),
                articles
            )
            self.log.info("Crawled data is inserted!!")
            
            conn.execute(
                text(f"UPDATE HEADLINE SET last_update = '{str(last_update)}' WHERE country_code = '{self.country_code}'")
            )
            self.log.info("last_update of DB is updated!!")
            

class ArchiveOldArticles(BaseOperator, LoggingMixin):
    
    def __init__(
        self,
        db_conn_str:str,
        country_code:str,
        *args,
        **kwargs):
        """
        THIS IS ACTION PER COUNTRY !!!
        
        1. finds old articles, which is not exist in gnews headline, from the table `HEADLINE_ARTICLES`.
        2. move the articles to the table ARCHIVED_ARTICLES.

        Args:
            db_conn_str (str): _description_
            country_code (str): _description_
        """
        
        super(ArchiveOldArticles, self).__init__(*args, **kwargs)
        
        self.db_conn_str = db_conn_str
        self.country_code = country_code
        
    def execute(self, context):
        
        hook = DBHook(self.db_conn_str)
        engine = hook.get_engine()
        
        with engine.begin() as conn:            
            conn.execute(
                f"""
                IF EXISTS (
                    SELECT url 
                    FROM CRAWLED_ARTICLES 
                    WHERE country_code = '{self.country_code}'
                )
                BEGIN
                    INSERT INTO ARCHIVED_ARTICLES(country_code,url,title,description,image_url,publish_date,source)
                    SELECT
                        country_code,
                        url,
                        title,
                        description,
                        image_url,
                        publish_date,
                        source
                    FROM 
                        HEADLINE_ARTICLES ha 
                    WHERE
                        url NOT IN (
                            SELECT url 
                            FROM CRAWLED_ARTICLES 
                            WHERE country_code = '{self.country_code}'
                        )
                        AND url NOT IN (
                            SELECT url 
                            FROM ARCHIVED_ARTICLES 
                            WHERE country_code = '{self.country_code}'
                        );
                END
                """
            )
            self.log.info("Inserting old articles into archived articles is done!")
            
            conn.execute(
                f"""
                IF EXISTS (
                    SELECT url 
                    FROM CRAWLED_ARTICLES 
                    WHERE country_code = '{self.country_code}'
                )
                BEGIN
                    DELETE 
                    FROM 
                        HEADLINE_ARTICLES
                    WHERE
                        url NOT IN (
                            SELECT url 
                            FROM CRAWLED_ARTICLES 
                            WHERE country_code = '{self.country_code}'
                        )
                        AND country_code = '{self.country_code}'
                END
                """
            )
            self.log.info("deleting old articles from headline articles is done!")
            
class InsertNewArticles(BaseOperator, LoggingMixin):
    
    def __init__(
        self,
        db_conn_str:str,
        country_code:str,
        *args,
        **kwargs):
        """
        THIS IS ACTION PER COUNTRY !!!

        Args:
            db_conn_str (str): _description_
            country_code (str): _description_
        """

        super(InsertNewArticles, self).__init__(*args, **kwargs)
        self.db_conn_str = db_conn_str
        self.country_code = country_code
        
    def execute(self, context):
        
        hook = DBHook(self.db_conn_str)
        engine = hook.get_engine()
        
        with engine.begin() as conn:
            
            conn.execute(
                text(
                f"""
                INSERT INTO HEADLINE_ARTICLES(country_code,url,title,description,image_url,publish_date,source)
                SELECT 
                    ca.country_code,
                    ca.url,
                    ca.title,
                    ca.description,
                    ca.image_url,
                    ca.publish_date,
                    ca.source
                FROM 
                    CRAWLED_ARTICLES ca 
                WHERE
                    ca.country_code = N'{self.country_code}' 
                    AND
                    ca.url 
                        NOT IN (
                                SELECT url
                                FROM HEADLINE_ARTICLES
                                WHERE country_code = '{self.country_code}'
                            )
                """
                )
            )
            
class DeleteCrawledArticles(BaseOperator, LoggingMixin):
    
    def __init__(
        self,
        db_conn_str:str,
        country_code:str,
        *args,
        **kwargs):
        """
        THIS IS ACTION PER COUNTRY !!!

        Args:
            db_conn_str (str): _description_
            country_code (str): _description_
        """

        super(DeleteCrawledArticles, self).__init__(*args, **kwargs)
        self.db_conn_str = db_conn_str
        self.country_code = country_code
        
    def execute(self, context):
        
        hook = DBHook(self.db_conn_str)
        engine = hook.get_engine()
        
        with engine.begin() as conn:
            
            conn.execute(
                text(
                f"""
                DELETE FROM CRAWLED_ARTICLES
                WHERE country_code = '{self.country_code}'    
                """
                )
            )
            
class PullGithubRepo(BaseOperator, LoggingMixin):
    
    def __init__(
        self,
        task_id,
        repo_conn_str:str,
        repo_dir_path:str,
        *args, 
        **kwargs
    ):
        """
        1. If the repo_dir_path not existing folder, clone the repo there.
        2. Pull repo

        Args:
            repo_conn_str (str): _description_
            repo_dir_path (str): _description_
        """
        super(PullGithubRepo, self).__init__(task_id = task_id, *args, **kwargs)
        self.repo_conn_str = repo_conn_str
        self.repo_dir_path = repo_dir_path
        
    def execute(self, context):
        
        self.log.info(f"The repository will be placed to {self.repo_dir_path}")
        
        os.system(f"rm -r {self.repo_dir_path}")
        os.system(f"git clone {self.repo_conn_str} {self.repo_dir_path}")
        
        self.log.info("Pulling repository is done!")
        
        
            
            
class ExportDB(BaseOperator, LoggingMixin):
    
    def __init__(
        self,
        db_conn_str:str,
        country_code:str,
        dest_dir_path:str,
        *args,
        **kwargs
    ):
        """
        THIS IS ACTION PER COUNTRY !!!

        Args:
            db_conn_str (str): _description_
            country_code (str): _description_
            dest_dir_path (str): _description_
        """
        
        super(ExportDB, self).__init__(*args, **kwargs)
        
        self.db_conn_str = db_conn_str
        self.country_code = country_code
        
        if not os.path.exists(dest_dir_path):
            os.makedirs(dest_dir_path)
        self.export_path = os.path.join(dest_dir_path, f"{country_code}.csv")
        
    def execute(self, context):
        
        hook = DBHook(self.db_conn_str)
        engine = hook.get_engine()
        
        result = None
        with engine.begin() as conn:
            
            result = conn.execute(
                text(
                f"""
                SELECT 
                    country_code,
                    url,
                    title,
                    description,
                    image_url,
                    publish_date,
                    source
                FROM
                    HEADLINE_ARTICLES
                WHERE 
                    country_code = '{self.country_code}'
                """
                )
            ).all()
            
        assert type(result) is list, f"{type(result)} is not list!"    
        with open(self.export_path, "w") as file:
                
            file.write("country_code\turl\ttitle\tdescription\timage_url\tpublish_date\tsource")
            len_cols = 7
                
            for row in result:
                assert len(row) == len_cols
                formatted_row:str = '\n'
                    
                for idx, val in enumerate(row):
                        
                    val = str(val)
                        
                    val = val.replace('\t', ' ')
                    formatted_row += val
                        
                    if idx != len_cols - 1:
                        formatted_row += '\t'
                            
                assert formatted_row.count('\t', 0, len(formatted_row))
                file.write(formatted_row)
            
class ExportMetadata(BaseOperator, LoggingMixin):
    
    def __init__(
        self,
        db_conn_str:str,
        dest_dir_path:str,
        *args,
        **kwargs
    ):
        super(ExportMetadata, self).__init__(*args, **kwargs)
        
        self.db_conn_str = db_conn_str
        
        if not os.path.exists(dest_dir_path):
            os.makedirs(dest_dir_path)
            
        self.export_path_country_codes = os.path.join(dest_dir_path, "country_codes.json")
        self.export_path_headline_metadata = os.path.join(dest_dir_path, "headline_metadata.json")
    
    def execute(self, context):
        
        hook = DBHook(self.db_conn_str)
        metadata_list = hook.get_metadata()
        
        country_codes = []
        headline_metadata = {}
        
        for metadata in metadata_list:
            country_codes.append(metadata['country_code'])
            headline_metadata[metadata['country_code']] = {
                "country_name": metadata['country_name'],
                "last_update": str(metadata['last_update'])
            }


        with open(self.export_path_country_codes, "w") as file:
            json_str = json.dumps(country_codes)
            file.write(json_str)
            
            self.log.info("Exporting country_code.json done!")
            
        with open(self.export_path_headline_metadata, "w") as file:
            json_str = json.dumps(headline_metadata)
            file.write(json_str)
            
            self.log.info("Exporting headline_metadata.json done!")
            
        
            
    
class UpdateGithubRepo(BaseOperator, LoggingMixin):
    
    def __init__(
        self,
        repo_dir_path:str,
        *args, 
        **kwargs
    ):
        super(UpdateGithubRepo, self).__init__(*args, **kwargs)
        self.repo_dir_path = os.path.realpath(repo_dir_path)
        
    def execute(self, context):
        
        command = f"""cd {self.repo_dir_path} && \
            git add . && \
            git config --global user.email \"world.headlines.0@gmail.com\" && \
            git config --global user.name \"Wonbin Kim\"
            git commit -m "data updated" && \
            git push origin main
        """
        
        result = subprocess.check_output(command, shell=True, text=True)
        self.log.info(result)
            