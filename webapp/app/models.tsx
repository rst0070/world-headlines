class NewsArticle{
    url: string
    country: string
    source: string
    title: string
    description: string
    image_url: string
    publish_date: string
    src_lang: string

    constructor(
        url: string,
        country: string,
        source: string,
        title: string,
        description: string,
        image_url: string,
        publish_date: string,
        src_lang: string,
    ){
        this.url = url;
        this.country = country
        this.source = source
        this.title = title
        this.description = description
        this.image_url = image_url
        this.publish_date = publish_date
        this.src_lang = src_lang
    }  

}

class Headline{
    country: string
    country_code: string
    src_lang: string
    url: string
    last_update: string
    articles: NewsArticle[]

    constructor(
        country: string,
        country_code: string,
        src_lang: string,
        url: string,
        last_update: string,
        articles: NewsArticle[]
    ){
        this.country = country
        this.country_code = country_code
        this.src_lang = src_lang
        this.url = url
        this.last_update = last_update
        this.articles = articles
    }
}

class GlobalData {

    countryNames: string[];
    countryCodes: string[];
    headlineMap: Map<string, Headline>;
    noImageUrl: string;

    constructor(
        countryNames: string[],
        countryCodes: string[],
        headlineMap: Map<string, Headline>,
        noImageUrl: string
    ){
        this.countryNames = countryNames;
        this.countryCodes = countryCodes;
        this.headlineMap = headlineMap;
        this.noImageUrl = noImageUrl;
    }
}
export {Headline, NewsArticle, GlobalData}