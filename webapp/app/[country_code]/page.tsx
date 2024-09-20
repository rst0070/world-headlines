import GlobalData from "../app.data";
import Image from "next/image"; 
import { Headline, NewsArticle } from "../models";

export async function generateStaticParams(): Promise<object[]> {

    let params: object[] = []

    return new Promise((res, rej) => {
        GlobalData.country_codes.forEach((code: String, idx:number, arr:string[]) =>{
            params.push({country_code : code})
            if(idx == arr.length - 1){
                res(params)
            }
        })
    })
}

function getNewsItem(article: NewsArticle){
    
    return (
            <div className="news-item" id={article.url + article.title}>
                <img src={article.image_url} alt="" width={280} height={168}/>
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

export default async function Page({ params }: { params: { country_code: string } }) {
    let code: string = params.country_code.charAt(0).toUpperCase() + params.country_code.charAt(1).toUpperCase()

    let headline: Headline = GlobalData.headline_map.get(code)
    let news = []

    return new Promise((resolve, reject) =>{
        headline.articles.forEach((v, i, a)=>{
            news.push(getNewsItem(v))
            if(i == a.length - 1){
                resolve((
                    <main>
                        {/* <div id="google_translate_element"></div> */}
                        <div className="news-section">
                            {news}
                        </div>
                        {/* <script type="text/javascript">
                            {`
                            function googleTranslateElementInit() {
                            new google.translate.TranslateElement({pageLanguage: 'en', autoDisplay: true}, 'google_translate_element');
                            }
                            `}
                        </script> */}
                    </main>
                    
                ))
            }
        })
    })
}