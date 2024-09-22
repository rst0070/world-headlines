from config import Config
from services import is_gnews_updated, update_db
from typing import List, Tuple


def load_configs():
    """
    Updates basic headline information to the Config obj
    The information will be used for inserting news articles
    """
    
    Config.db_cursor = Config.db_connection.cursor()
    
    ### 
    res: List[Tuple[str, str]] = Config.db_cursor.execute("SELECT country, src_lang FROM HEADLINE").fetchall()
    
    for country, src_lang in res:
        assert type(country) is str
        assert type(src_lang) is str
        
        Config.country_names.append(country)
        Config.src_lang_by_counrty[country] = src_lang

def check_n_update():
    """
    1. Check "is updating headline in DB needed?"
    2. If it is needed, updated db
    """
    
    for country in Config.country_names:
        print(f"Check n Update: {country}")
        
        if is_gnews_updated(country):
            update_db(country)
       