import type { NewsArticle } from "../types/NewsArticle";
import { subDays } from "date-fns";


type NewsArticleResponse = {
    country_code: string;
    url: string;
    title: string;
    description: string;
    image_url: string;
    publish_date: string;
    source: string;
    en_title: string;
    en_description: string;
    en_topics: string[];
    en_keywords: string[];
}

export async function getWorldSnapshot(): Promise<NewsArticle[]>{
    let response = await fetch(`/api/v1/news/world_snapshot`)
    let data = (await response.json()) as {data: NewsArticleResponse[]}

    return data.data.map(val => ({
        countryCode: val.country_code,
        url: val.url,
        title: val.title,
        description: val.description,
        imageUrl: val.image_url,
        publishDate: val.publish_date,
        source: val.source,
        enTitle: val.en_title,
        enDescription: val.en_description,
        enTopics: val.en_topics,
        enKeywords: val.en_keywords
    }))
}

export async function getNewsArticles(countryCode:string): Promise<NewsArticle[]>{
    const nowDate = new Date();
    const fromDate = subDays(nowDate, 1).toISOString();
    const toDate = nowDate.toISOString();

    let response = await fetch(`/api/v1/news/articles?countryCode=${countryCode}&fromDate=${fromDate}&toDate=${toDate}&size=20`)

    let dataList = await response.json() as {data: NewsArticleResponse[]}

    let result:NewsArticle[] = []

    dataList.data.forEach(val => {
        result.push({
            countryCode: val.country_code,
            url: val.url,
            title: val.title,
            description: val.description,
            imageUrl: val.image_url,
            publishDate: val.publish_date,
            source: val.source,
            enTitle: val.en_title,
            enDescription: val.en_description,
            enKeywords: val.en_keywords
        })
    })

    return result;
}