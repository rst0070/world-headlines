import Image from "next/image"; 
import { NewsArticle } from "@/types/NewsArticle";
import { CountryHeadline } from "@/types/CountryHeadline";
import { ReactNode } from "react";
import NewsItem from "@/components/NewsItem";
import {getHeadlineInfo, getNewsArticles} from "@/services/api/country"


export default async function Page(props: { params: Promise<{ countryCode: string }> }) {

    const { countryCode } = await props.params;
    const newsArticleList:NewsArticle[]    = await getNewsArticles(countryCode)
    const headlineMetadata:CountryHeadline = await getHeadlineInfo(countryCode)

    let newsArticleElements: ReactNode[] = []
    await Promise.all(newsArticleList.map(
        (val, idx, arr) => {
            const element = (<NewsItem newsArticle={val} noImageUrl="https://example.com/empty.png" key={idx}></NewsItem>);
            newsArticleElements.push(element)
        }
    ))

    const result = (
        <>
            <section className="headline-info">
                <section className="headline-desc">
                    <Image src={"/flags/"+countryCode+".svg"} alt={""} width={100} height={75}/>
                    <ul>
                        <li>Latest headline news from {headlineMetadata.countryName}.</li>
                        <li>The headline updated at <span id="last-update-headline">{headlineMetadata.lastUpdate}</span></li>
                    </ul>
                </section>
            </section>
            <main className="news-section">
                {newsArticleElements}
            </main>
        </>
    )


    return new Promise(
        async (resolve, reject) =>{
            resolve(result)
        }
    )
}