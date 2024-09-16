import deepl
from models import HeadLine, NewsArticle
from repositories import DBRepository, GNewsRepository
from datetime import datetime
from typing import List, Tuple
from config import Config


def translate_news_article(
        news_article: NewsArticle,
        target_lang: str,
        source_lang: str
    ):
    
        return NewsArticle(
            url             = news_article.url,
            country         = news_article.country,
            source          = news_article.source,
            title           = Config.deepl_translator.translate_text(news_article.title, source_lang=source_lang, target_lang=target_lang),
            image_url       = news_article.image_url,
            publish_date    = news_article.publish_date,
            src_lang        = news_article.src_lang,
            target_lang     = target_lang
        )   


def is_gnews_updated(country_name:str):
    assert country_name in Config.country_names, f"{country_name} is not config.Config.country_names"
    
    db_last_update = DBRepository.get_last_update_of_headline(country_name)
    
    gnews_last_update = GNewsRepository.get_last_update_of_headline(country_name)
    
    return db_last_update != gnews_last_update
    
def update_db(country_name:str):
    """

    Args:
        country_name (str): _description_
        
    1. Get headline from GNews
    2. Delete articles from new headline, which is already exist 
    3. Delete articles from DB, which is no longer on headline
    4. Translate articles
    4. insert new articles
    """
    
    print(f"updating db for {country_name} ----------------------------------------------------")
    headline: HeadLine = GNewsRepository.get_headline(country_name)

    old_urls = DBRepository.get_urls_of_articles(country_name)
    new_urls = [article.url for article in headline.articles]
    
    articles_to_save = []
    urls_to_delete: List[Tuple[str]] = []
    
    
    ### ---------------------------------------------------- Delete old Articles
    for url in old_urls:
        if url not in new_urls:
            urls_to_delete.append((url,))
    
    DBRepository.delete_articles_by_urls(urls_to_delete)
    
    
    ### ---------------------------------------------------- Select Articles to store
    for article in headline.articles:
        if article.url not in old_urls:
            articles_to_save.append(article)
    
    ### ---------------------------------------------------- Translate Articles
    print("translating articles...")
    origin_len = len(articles_to_save)
    
    for idx in range(0, origin_len):
        
        origin:NewsArticle = articles_to_save[idx]
        
        for target_lang in Config.target_langs:
            if origin.target_lang == target_lang:
                continue
            
            translated = translate_news_article(
                origin, target_lang, origin.src_lang
            )
            
            articles_to_save.append(translated)
    print("OK")
    ### ---------------------------------------------------- Store Articles
    DBRepository.insert_news_articles(articles_to_save)
    print("update complete")
    
    