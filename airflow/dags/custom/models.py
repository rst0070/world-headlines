
class NewsArticle:
    
    def __init__(
        self,
        country_code,
        url,
        title,
        description,
        image_url,
        publish_date,
        source
    ):
        
        self.country_code = country_code
        self.url = url
        self.title = title
        self.description = description
        self.image_url = image_url
        self.publish_date = publish_date
        self.source = source