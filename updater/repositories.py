import requests
import xml.etree.ElementTree as ET
from typing import List, Tuple
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from models import HeadLine, NewsArticle
from config import Config
from tqdm import tqdm


class DBRepository:
    
    @classmethod
    def get_headline_url(cls, country_name: str) -> str:
        
        res = Config.db_cursor.execute(
            f"SELECT url FROM HEADLINE WHERE country = '{country_name}'"
        )
        
        url = res.fetchone()[0]
        
        return url
    
    @classmethod
    def get_last_update_of_headline(cls, country_name:str) -> str:
        """
        returns last update of headline which is on DB
        """
        
        res = Config.db_cursor.execute(
            f"SELECT last_update FROM HEADLINE WHERE country = '{country_name}'"
        )
        
        last_update = res.fetchone()[0]
        
        return last_update
    
    @classmethod
    def update_last_update_of_headline(cls, country_name:str, last_update:str):
        """
        updates last update of a headline
        """
        Config.db_cursor.execute(
            f"UPDATE HEADLINE SET last_update = '{last_update}' WHERE country = '{country_name}'"
        )
        
        Config.db_connection.commit()

    @classmethod
    def get_urls_of_articles(cls, country_name:str) -> List[str]:
       
       res: List[Tuple[str]] = Config.db_cursor.execute(
           f"SELECT DISTINCT url FROM NEWS_ARTICLES WHERE country = '{country_name}'"
       ).fetchall()
       
       urls = [tup[0] for tup in res]
       
       return urls


    @classmethod
    def insert_news_articles(cls, news_articles: List[NewsArticle]):
        
        batch = []
        
        for i in news_articles:
            batch.append(
                (i.url, i.country, i.source, i.title, i.description, i.image_url, i.publish_date, i.src_lang)
            )
        
        Config.db_cursor.executemany(
            """
            INSERT INTO NEWS_ARTICLES(url, country, source, title, description, image_url, publish_date, src_lang) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?)
            """,
            batch
        )
        Config.db_connection.commit()
        batch.clear()
    
    
    @classmethod
    def delete_articles_by_country_n_urls(cls, country_name:str, urls: List[str]):
        
        batch: List[Tuple[str, str]] = [(country_name, url) for url in urls]
        
        Config.db_cursor.executemany(
            "DELETE FROM NEWS_ARTICLES WHERE country = ? AND url = ?",
            batch
        )
        Config.db_connection.commit()



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
        
        def getDeepInfo(redirect_url:str) -> Tuple[str, str, str]:
            """
            Using redirect_url google providing, redirect it to get to original article.
            In there, get detailed information: article original url, image url, description

            Args:
                redirect_url (str): url for making web browser redirect to google.

            Returns:
                Tuple[str, str, str]: article original url, image url, description
            """
            _driver.get(url = redirect_url)
            WebDriverWait(_driver, Config.crawling_timeout_per_article).until_not(EC.url_contains('google.com'))

            # --------------- get original article url
            article_url: str = _driver.current_url
            # --------------- get image url
            image_url: str = Config.news_empty_img_url
            try:
                image_url = _driver.find_element(By.XPATH, "//meta[@property='og:image']").get_attribute('content')
                if image_url is None:
                    image_url = Config.news_empty_img_url
            except:
                pass
            # --------------- get description
            description: str = ''
            try:
                description = _driver.find_element(By.XPATH, "//meta[@property='og:description']").get_attribute('content')
                if description is None:
                    description = ''
            except:
                pass
            
            return article_url, image_url, description
        
        
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
            description     = ''
            
            try:
                article_url, img_url, description = getDeepInfo(article_url)
            except:
                pass
            
            articles.append(
                NewsArticle(
                    url             = article_url,
                    country         = country_name,
                    source          = item.find('source').text,
                    title           = item.find('title').text,
                    description     = description,
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
        