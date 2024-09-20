import getGlobalData from "../app.data";
import Image from "next/image"; 
import { Headline, NewsArticle, GlobalData } from "../models";
import { ReactNode } from "react";

export async function generateStaticParams(): Promise<object[]> {

    let params: object[] = []

    return new Promise(async (res, rej) => {
        let data = await getGlobalData()

        data.countryCodes.forEach((code: String, idx:number, arr:string[]) =>{
            params.push({country_code : code})
            if(idx == arr.length - 1){
                res(params)
            }
        })
    })
}

/**
 * 
 * @param article 
 * @returns 
 */
async function getNewsItem(article: NewsArticle): Promise<ReactNode>{


    return new Promise(async (resolve, reject)=>{
        let data = await getGlobalData()
        let image_tag = <></>;
        if(article.image_url != data.noImageUrl)
            image_tag = <img src={article.image_url} alt="" width={280} height={168}/>;
        
        resolve(
            <div className="news-item" key={article.url + article.title}>
                {image_tag}
                <div className="news-details">
                    <h3><a href={article.url} target="_blank">{article.title}</a></h3>
                    <p>{article.publish_date}</p>
                    <p>{article.description}</p>
                    <ul className="sources">
                        <li><a href="#">{article.source}</a></li>
                    </ul>
                </div>
            </div>
        )
    })
}

export default async function Page({ params }: { params: { country_code: string } }) {
    let code: string = params.country_code.charAt(0).toUpperCase() + params.country_code.charAt(1).toUpperCase()

    let data = await getGlobalData()
    console.log(code)

    if(!data.headlineMap.has(code))
        console.log("OHHHH MY GODDDDD")

    let headline = data.headlineMap.get(code)
    let news = []

    return new Promise(async (resolve, reject) =>{

        if(headline == undefined){
            reject("headline is undefined")
        }else{
            headline.articles.forEach(async (v, i, a)=>{
                news.push(await getNewsItem(v))
                if(i == a.length - 1){
    
                    if(news == undefined){
                        reject("news is undefined")
                    }else
                        resolve((
                            <>
                                <section className="headline-info">
                                    <p>latest headline news from {v.country}.</p>
                                    <p>The headline updated at {headline.last_update}</p>
                                </section>
                                <main className="news-section">
                                    {news}
                                </main>
                            </>
                        ))
                }
            })
        }
    })
}