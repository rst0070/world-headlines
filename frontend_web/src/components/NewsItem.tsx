import { ReactNode } from "react";
import { NewsArticle } from "@/types/NewsArticle";

/**
 * 
 * @param article 
 * @returns 
 */
export default function NewsItem(
        {newsArticle, noImageUrl}:{newsArticle:NewsArticle, noImageUrl:string}
    ): ReactNode {

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