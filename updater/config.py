from typing import List, Dict
import sqlite3

class Config:
    
    db_connection = sqlite3.connect('world_headline.db')
    news_empty_img_url = "https://via.placeholder.com/150"
    
    country_names: List[str] = []
    src_lang_by_counrty: Dict[str, str] = {}
    