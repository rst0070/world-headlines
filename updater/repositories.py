import requests
import xml.etree.ElementTree as ET
from typing import List, Tuple
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
from models import HeadLine, NewsArticle
from config import Config
from tqdm import tqdm


class DBRepository:
    
    _conn: sqlite3.Connection = Config.db_connection
    _cursor = _conn.cursor()
    
    @classmethod
    def get_headline_url(cls, country_name: str) -> str:
        
        res = cls._cursor.execute(
            f"SELECT url FROM HEADLINE WHERE country = '{country_name}'"
        )
        
        url = res.fetchone()[0]
        
        return url
    
    @classmethod
    def get_last_update_of_headline(cls, country_name:str) -> str:
        """
        returns last update of headline which is on DB
        """
        
        res = cls._cursor.execute(
            f"SELECT last_update FROM HEADLINE WHERE country = '{country_name}'"
        )
        
        last_update = res.fetchone()[0]
        
        return last_update
    
    @classmethod
    def update_last_update_of_headline(cls, country_name:str, last_update:str)->str:
        """
        updates last update of a headline
        """
        cls._cursor.execute(
            f"UPDATE HEADLINE SET last_update = '{last_update}' WHERE country = '{country_name}'"
        )
        cls._conn.commit()

    @classmethod
    def get_urls_of_articles(cls, country_name:str) -> List[str]:
       
       res: List[Tuple[str]] = cls._cursor.execute(
           f"SELECT DISTINCT url FROM NEWS_ARTICLES WHERE country = '{country_name}'"
       ).fetchall()
       
       urls = [tup[0] for tup in res]
       
       return urls


    @classmethod
    def insert_news_articles(cls, news_articles: List[NewsArticle]):
        
        batch = []
        
        for i in news_articles:
            batch.append(
                (i.url, i.country, i.source, i.title, i.image_url, i.publish_date, i.src_lang)
            )
        
        cls._cursor.executemany(
            """
            INSERT INTO NEWS_ARTICLES(url, country, source, title, image_url, publish_date, src_lang) 
                VALUES(?, ?, ?, ?, ?, ?, ?)
            """,
            batch
        )
        cls._conn.commit()
        batch.clear()
    
    
    @classmethod
    def delete_articles_by_urls(cls, urls: List[str]):
        
        cls._cursor.executemany(
            "DELETE FROM NEWS_ARTICLES WHERE url = ?",
            urls
        )
        cls._conn.commit()



class GNewsRepository:
    """
    Provides information(and Model) from Google News. 
    
    """
    
    @classmethod
    def get_last_update_of_headline(cls, country_name:str) -> str:
        
        gnews_url = DBRepository.get_headline_url(country_name)
        
        rss_req = requests.get(gnews_url)
        xml_root = ET.fromstring(rss_req.text)
        last_update_str = xml_root.find('channel').find('lastBuildDate').text
        
        #last_update = datetime.strptime(last_update_str, "%a, %d %b %Y %H:%M:%S %Z")
        
        return last_update_str        
    
    
    @classmethod
    def get_headline(cls, country_name:str) -> HeadLine:
        
        
        src_lang = Config.src_lang_by_counrty[country_name]
        
        gnews_url = DBRepository.get_headline_url(country_name)
        
        _options = Options()  
        _options.add_argument('--headless')
        _driver = webdriver.Firefox(options=_options)
        
        def getNewsUrls(redirect_url:str) -> Tuple[str, str]:
            """
            This is a function only used in this constructor
            Args:
                article_url (str): url of news article. it has redirection form of google news url

            Returns:
                str: img url of the news article
            """
            _driver.get(url = redirect_url)
            WebDriverWait(_driver, 5).until_not(EC.url_contains('google.com'))

            article_url = _driver.current_url
            element = _driver.find_element(By.XPATH, "//meta[@property='og:image']")
            
            return article_url, element.get_attribute('content')
        
        
        ####################################################################
        ### Using RSS request(XML parsing), save articles information
        ####################################################################
        
        
        rss_req = requests.get(gnews_url)
        xml_root = ET.fromstring(rss_req.text)
        
        articles: List[NewsArticle] = []
        last_update: str = xml_root.find('channel').find('lastBuildDate').text
        
        for item in tqdm(xml_root.find('channel').findall('item'), desc=f"crawling headline of {country_name}"):
            
            article_url     = item.find('link').text
            img_url         = Config.news_empty_img_url
            try:
                article_url, img_url = getNewsUrls(article_url)
            except:
                pass
            
            articles.append(
                NewsArticle(
                    url             = article_url,
                    country         = country_name,
                    source          = item.find('source').text,
                    title           = item.find('title').text,
                    image_url       = img_url,
                    publish_date    = item.find('pubDate').text,
                    src_lang        = src_lang
                )
            )
            
        _driver.quit()
        
        return HeadLine(
            country_name=country_name,
            src_lang = src_lang,
            articles=articles,
            last_update=last_update,
            gnews_url=gnews_url    
        )
        