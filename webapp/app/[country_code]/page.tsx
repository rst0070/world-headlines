import GlobalData from "../app.data";
import Image from "next/image"; 
import { Headline, NewsArticle } from "../models";

export async function generateStaticParams() {

    let params: object[] = []

    GlobalData.country_codes.forEach((code: String, idx:number, arr:string[]) =>{
        params.push({country_code : code})
    })
    return params
}

function getNewsItem(article: NewsArticle){
    
    return (
        <div className="news-item">
                <Image src={article.image_url} alt="" width={280} height={168}/>
                <div className="news-details">
                    <h3><a href={article.url}>{article.title}</a></h3>
                    <p>{article.publish_date}</p>
                    <p>{article.description}</p>
                    <ul className="sources">
                        <li><a href="#">{article.source}</a></li>
                    </ul>
                </div>
        </div>
    )
}

export default function Page({ params }: { params: { country_code: string } }) {
    let code: string = params.country_code.charAt(0).toUpperCase() + params.country_code.charAt(1).toUpperCase()

    let headline: Headline = GlobalData.headline_map.get(code)

    let news = []

    console.log(headline)
    headline.articles.forEach((v, i, a)=>{
        news.push(getNewsItem(v))
    })

    return (
        <section className="news-section">
            {news}
        </section>
    )
}