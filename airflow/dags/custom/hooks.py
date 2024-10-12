from typing import List, Tuple
from airflow.hooks.base import BaseHook
from airflow.utils.log.logging_mixin import LoggingMixin

from sqlalchemy.engine import Engine
from sqlalchemy import create_engine, text

from custom.models import NewsArticle
import datetime

import requests
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from custom import scripts

class DBHook(BaseHook):
    
    def __init__(self, conn_str, *args, **kwargs):
        
        super(DBHook, self).__init__(*args, **kwargs)
        
        self.engine = create_engine(conn_str)
        
    def get_engine(self) -> Engine:
        return self.engine
    
    def get_metadata(self) -> List[dict]:
        """
        Returns
        
            List[dict]: e.g. [{'country_code' : v1,'country_name' : v2, 'url' : v3}, ...]
        """
        with self.engine.begin() as conn:
            
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
        
class CrawlHeadlineHook(BaseHook, LoggingMixin):
    
    def __init__(
        self,
        gnews_url:str,
        country_code:str,
        crawl_max_num: int,
        crawl_timeout_sec: float,
        *args,
        **kwargs
        ):
        super(CrawlHeadlineHook, self).__init__(*args, **kwargs)
        
        self.gnews_url = gnews_url
        self.country_code = country_code
        self.crawl_max_num = crawl_max_num
        self.crawl_timeout_sec = crawl_timeout_sec
        
    def crawl(self) -> Tuple[List[NewsArticle], datetime.datetime]:
        
        
        gnews_article_list, last_update  = self._get_gnews_article_list(self.gnews_url, self.crawl_max_num)
        
        crawled_article_list: List[NewsArticle] = []
        driver = self._get_webdriver()
        
        for idx, gnews_article in enumerate(gnews_article_list):
            
            try:
                url, image_url, description = self._get_article_info(driver, gnews_article.url)
                # selenium.common.exceptions.TimeoutException
                if url is not None:
                    gnews_article.url = url
                if image_url is not None:
                    gnews_article.image_url = image_url
                if description is not None:
                    gnews_article.description = description
            except Exception as e:
                self.log.error("couldn't get detail info of article "+repr(e))
            finally:
                crawled_article_list.append(gnews_article)
                self.log.info(f"crawling status: {idx+1}/{len(gnews_article_list)} done.")      
            
        driver.quit()
        
        return crawled_article_list, last_update
    
    def _get_gnews_article_list(self, gnews_url, crawl_max_num) -> Tuple[List[NewsArticle], datetime.datetime]:
        
        self.log.info(f"getting rss from... {gnews_url}")
        
        rss_req = requests.get(gnews_url)
        xml_root = ET.fromstring(rss_req.text)
        
        article_list: List[NewsArticle] = []
        last_update = scripts.gnews_gmt_str_to_datetime(xml_root.find('channel').find('lastBuildDate').text)
        
        for idx, item in enumerate(xml_root.find('channel').findall('item')):
            
            if idx >= crawl_max_num:
                break
            
            article = NewsArticle(
                country_code=self.country_code,
                url = item.find('link').text,
                title = item.find('title').text,
                description = None,
                image_url=None,
                publish_date=scripts.gnews_gmt_str_to_datetime(item.find('pubDate').text),
                source=item.find('source').text
            )
            
            article_list.append(article)
            
        self.log.info(f"Completed getting info from... {gnews_url}")
        
        return (article_list, last_update)
                
        
        
    def _get_webdriver(self) -> webdriver.Firefox:
        
        options = webdriver.FirefoxOptions()  
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        
        return driver
    
    def _get_article_info(
        self, 
        driver:webdriver.Firefox, 
        gnews_article_url:str
        ) -> Tuple[str|None, str|None, str|None]:

        # --------------- wait until get into original article url
        driver.get(url = gnews_article_url)
        WebDriverWait(driver, self.crawl_timeout_sec).until_not(EC.url_contains('google.com'))
        
        article_url: str|None = driver.current_url
        image_url: str|None = None
        description: str|None = None
        
        if article_url in ('about:blank',):
            article_url = None
        
        try:
            image_url = driver.find_element(By.XPATH, "//meta[@property='og:image']").get_attribute('content')
        except Exception as e:
            self.log.error("couldn't get image url: " + repr(e))
            
        try:
            description = driver.find_element(By.XPATH, "//meta[@property='og:description']").get_attribute('content')
        except Exception as e:
            self.log.error("couldn't get description: " + repr(e))
            
        return article_url, image_url, description 