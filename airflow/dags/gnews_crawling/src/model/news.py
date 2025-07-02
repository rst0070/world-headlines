from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class NewsArticle:
    country_code: str
    url: str
    title: str
    description: str
    image_url: str
    publish_date: datetime | str
    source: str

    en_title: Optional[str] = None
    en_description: Optional[str] = None
    
    @staticmethod
    def get_table_structure():
        return """
            country_code char(2),
            url TEXT,
            title TEXT,
            description TEXT,
            image_url TEXT,
            publish_date TIMESTAMP,
            source TEXT,

            en_title TEXT NULL,
            en_description TEXT NULL,

            PRIMARY KEY (country_code, url)
        """