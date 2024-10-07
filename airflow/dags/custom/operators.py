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
from airflow.utils.log.logging_mixin import LoggingMixin

from custom.hooks import MetadataHook
from custom.hooks import DBHook
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
        
        hook = DBHook(self.db_conn_str)
        
        articles, last_update = self._get_articles(self.gnews_url)
        
        engine = hook.get_engine()
        
        with engine.begin() as conn:
            
            conn.execute(
                text(
                """
                INSERT INTO CRAWLED_ARTICLES(country_code,url,title,description,image_url,publish_date,source)
                VALUES(:country_code,:url,:title,:description,:image_url,:publish_date,:source)
                """),
                articles
            )
            self.log.info("Crawled data is inserted!!")
            
            conn.execute(
                text(f"UPDATE HEADLINE SET last_update = '{str(last_update)}' WHERE country_code = '{self.country_code}'")
            )
            self.log.info("last_update of DB is updated!!")
            
            
        
    # def _get_headline_url(self, hook) -> str:
        
    #     engine = hook.get_engine()
    #     with engine.begin() as conn:
            
    #         url = conn.execute(text(f"SELECT url FROM HEADLINE WHERE country_code = '{self.country_code}'")).all()[0][0]
    #         assert type(url) is str
            
    #         return url
        
    def _get_articles(self, gnews_url) -> Tuple[List[dict], datetime.datetime]:
        
        ####################################################################
        ### Using RSS request(XML parsing), save articles information
        ####################################################################
        
        
        rss_req = requests.get(gnews_url)
        xml_root = ET.fromstring(rss_req.text)
        
        article_info_list: List[dict] = []
        last_update = scripts.gnews_gmt_str_to_datetime(xml_root.find('channel').find('lastBuildDate').text)
        
        driver = self._get_webdriver()
        #tqdm(xml_root.find('channel').findall('item'), desc=f"crawling headline of {country_name}"):
        # need to find a way to use tqdm for log            
        for idx, item in enumerate(xml_root.find('channel').findall('item')):
            
            if idx >= self.crawl_max_num:
                break
            
            article = {
                    "country_code"  :self.country_code,
                    "url"           : item.find('link').text, 
                    "title"         : item.find('title').text,
                    "description"   : None,
                    "image_url"     : None,
                    "publish_date"  : scripts.gnews_gmt_str_to_datetime(item.find('pubDate').text),
                    "source"        : item.find('source').text
                }
            
            try:
                article["url"], \
                article["image_url"], \
                article["description"] \
                    = self._get_article_info(driver, article["url"])
            except:
                self.log.warning("error occurred in _get_articles")
            
            
            article_info_list.append(article)
            
        driver.quit()
        
        return article_info_list, last_update
        
    def _get_webdriver(self) -> webdriver.Firefox:
        
        options = webdriver.FirefoxOptions()  
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        
        return driver
    
    def _get_article_info(
        self, 
        driver:webdriver.Firefox, 
        gnews_article_url:str,
        
        ) -> Tuple[str, str|None, str|None]:

        # --------------- wait until get into original article url
        driver.get(url = gnews_article_url)
        WebDriverWait(driver, self.crawl_timeout_sec).until_not(EC.url_contains('google.com'))
        
        article_url: str = driver.current_url
        image_url: str|None = None
        description: str|None = None
        
        try:
            image_url = driver.find_element(By.XPATH, "//meta[@property='og:image']").get_attribute('content')
            description = driver.find_element(By.XPATH, "//meta[@property='og:description']").get_attribute('content')
        except:
            self.log.warning("exception occurred in _get_artice_info")
            
        return article_url, image_url, description 
    

class DeleteOldArticles(BaseOperator, LoggingMixin):
    
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
        
        super(DeleteOldArticles, self).__init__(*args, **kwargs)
        
        self.db_conn_str = db_conn_str
        self.country_code = country_code
        
    def execute(self, context):
        
        hook = DBHook(self.db_conn_str)
        engine = hook.get_engine()
        
        with engine.begin() as conn:
            
            conn.execute(
                text(
                f"""
                DELETE FROM HEADLINE_ARTICLES
                WHERE url NOT IN (
                        SELECT url 
                        FROM CRAWLED_ARTICLES 
                        WHERE country_code = '{self.country_code}'
                    )
                """
                )
            )
            
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
        super(PullGithubRepo, self).__init__(*args, **kwargs)
        self.repo_conn_str = repo_conn_str
        self.repo_dir_path = repo_dir_path
        
    def execute(self, context):
        
        self.log.info(f"The repository will be placed to {self.repo_dir_path}")
        
        os.system(f"rm -r {self.repo_dir_path}")
        os.system(f"git clone {self.repo_conn_str} {self.repo_dir_path}")
        
        # if not os.path.isdir(os.path.join(self.repo_dir_path, '.git')):
        #     msg = os.popen(
        #         f"""mkdir -p {self.repo_dir_path} && \
        #         git clone {self.repo_conn_str} {self.repo_dir_path}
        #         """).read()
            
        #     self.log.info(msg)
        #     self.log.info("finished process cloning repository!")
        
        # msg = os.popen(
        # f"""cd {self.repo_dir_path} && \
        # git pull origin main              
        # """).read()
        # self.log.info(msg)
        
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
        
        hook = MetadataHook(self.db_conn_str)
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
        self.repo_dir_path = repo_dir_path
        
    def execute(self, context):
        
        command = f"""cd {self.repo_dir_path} && \
            git add . && \
            git config --global user.email \"world.headlines.0@gmail.com\" && \
            git config --global user.name \"Wonbin Kim\" && \
            git commit -m "data updated" && \
            git push origin main
        """
        result = subprocess.check_output(command, shell=True, text=True)
        self.log.info(result)