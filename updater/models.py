from typing import List

class NewsArticle:
    """
    Information of News Article
    """
    
    def __init__(
        self,
        url:str,
        country,
        source:str,
        title:str,
        description:str,
        image_url:str,
        publish_date:str,
        src_lang:str
    ):
        
        self.url            = url
        self.country        = country
        self.source         = source
        self.title          = title
        self.description    = description
        self.image_url      = image_url
        self.publish_date   = publish_date
        self.src_lang       = src_lang
        
        

class HeadLine:
    
    def __init__(
        self, 
        country_name:str, 
        src_lang:str,
        articles:List[NewsArticle],
        last_update:str,
        gnews_url:str            
    ):
        
        self.country_name: str           = country_name
        self.src_lang: str               = src_lang
        self.articles: List[NewsArticle] = articles
        self.last_update: str            = last_update
        self.gnews_url: str              = gnews_url
            
        