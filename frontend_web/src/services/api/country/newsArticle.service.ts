import { environment } from "@/environment";
import { NewsArticle } from "@/types/NewsArticle";

type NewsArticleResponse = {
    country_code: string;
    url: string;
    title: string;
    description: string;
    image_url: string;
    publish_date: string;
    source: string;
}

export async function getNewsArticles(countryCode:string): Promise<NewsArticle[]>{
    
    let response = await fetch(`${environment.backendApiUrl}/api/country/news_articles?country_code=${countryCode}`)

    let dataList = await response.json()

    let result:NewsArticle[] = []

    await Promise.all(
        dataList.map(
          (val: NewsArticleResponse , idx: number, arr: NewsArticleResponse[]) => {
              result.push({
                  countryCode: val['country_code'],
                  url: val['url'],
                  title: val['title'],
                  description: val['description'],
                  imageUrl: val['image_url'],
                  publishDate: val['publish_date'],
                  source: val['source']
              })
          }
        )
    )

    return new Promise((resolve, reject)=>{
      resolve(result);
    });
}