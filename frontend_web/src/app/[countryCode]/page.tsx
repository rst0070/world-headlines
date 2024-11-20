import Image from "next/image"; 
import { NewsArticle } from "@/types/NewsArticle";
import { CountryHeadline } from "@/types/CountryHeadline";
import { ReactNode } from "react";
import { Service } from "@/services/api/service";

/**
 * Generates parameters for static page.
 * The parameters are `country_codes` from `/data/country_codes.jon`
 * @returns 
 */
export async function generateStaticParams(): Promise<object[]> {

    const countryCodes = await Service.getCountryCodes()

    let param_list: object[] = [] 
    await Promise.all(
            countryCodes.map(
                async (code: string)=> param_list.push({countryCode : code})
                )
            )
    /**
     * e.g.
     * [
     *  {country_code: "us"},
     *  {country_code: "kr"},
     *  {country_code: "tw"}
     * ]
     */

    return new Promise(
        async (resolve, reject)=>{

            resolve(param_list)
        }
    )
}

/**
 * 
 * @param article 
 * @returns 
 */
function getNewsArticleElement(newsArticle:NewsArticle, noImageUrl:string): ReactNode {

    let image_tag = <></>;
    if(newsArticle.imageUrl != noImageUrl)
        image_tag = <img src={newsArticle.imageUrl} alt="" width={280} height={168}/>;

    return (
        <div className="news-item" key={newsArticle.url + newsArticle.title}>
            {image_tag}
            <div className="news-details">
                <h3><a href={newsArticle.url} target="_blank">{newsArticle.title}</a></h3>
                <p className="article-publish-date">{newsArticle.publishDate}</p>
                <p>{newsArticle.description}</p>
                <ul className="sources">
                    <li><a href="#">{newsArticle.source}</a></li>
                </ul>
            </div>
        </div>
    );
}


export default async function Page({ params }: { params: { countryCode: string } }) {

    const countryCode:string                = params.countryCode
    const newsArticleList:NewsArticle[]     = await Service.getNewsArticleList(countryCode)
    const headlineMetadata:CountryHeadline = await Service.getHeadlineMetadata(countryCode)

    let newsArticleElements: ReactNode[] = []
    await Promise.all(newsArticleList.map(
        (val, idx, arr) => {
            const element = getNewsArticleElement(val, 'None')
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