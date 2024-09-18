from models import HeadLine, NewsArticle
from repositories import DBRepository, GNewsRepository
from datetime import datetime
from typing import List
from config import Config
from tqdm import trange, tqdm

def is_gnews_updated(country_name:str) -> bool:
    """
    Check whether gnews last build date is newer than recorded in DB.
    
    Args:
        country_name (str): Should be in Config.country_names

    Returns:
        bool: boolean data
    """
    db_last_update: str = DBRepository.get_last_update_of_headline(country_name)
    
    gnews_last_update: str = GNewsRepository.get_last_update_of_headline(country_name)
    
    return db_last_update != gnews_last_update
    
def update_db(country_name:str):
    """

    Args:
        country_name (str): _description_
        
    1. Get headline from GNews
    2. Delete articles from new headline, which is already exist 
    3. Delete articles from DB, which is no longer on headline
    4. insert new articles
    5. update last_update of the headline
    """
    
    print(f"updating db for {country_name} ----------------------------------------------------")
    headline: HeadLine = GNewsRepository.get_headline(country_name)

    old_urls: List[str] = DBRepository.get_urls_of_articles(country_name)
    new_urls: List[str] = [article.url for article in headline.articles]
    
    articles_to_save: List[NewsArticle] = []
    urls_to_delete: List[str] = []
    
    ### ---------------------------------------------------- Delete old Articles
    for url in old_urls:
        assert type(url) is str
        
        if url not in new_urls:
            urls_to_delete.append(url)
    
    DBRepository.delete_articles_by_country_n_urls(country_name, urls_to_delete)
    print(f"deleting old articles is completed: total {len(urls_to_delete)}")
    urls_to_delete.clear()
    ### ---------------------------------------------------- Select Articles to store
    for article in headline.articles:
        if article.url not in old_urls:
            articles_to_save.append(article)
    
    ### ---------------------------------------------------- Store Articles
    DBRepository.insert_news_articles(articles_to_save)
    ### ---------------------------------------------------- Update last update of the headline
    DBRepository.update_last_update_of_headline(country_name, headline.last_update)
    print(f"update last_update of headline complete: {headline.last_update}")
    