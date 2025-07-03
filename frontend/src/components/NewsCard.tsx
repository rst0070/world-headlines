import type { NewsArticle } from "../types/NewsArticle";

interface NewsCardProps {
    newsArticle: NewsArticle;
}

const NewsCard: React.FC<NewsCardProps> = (props: NewsCardProps) => {
    const { newsArticle } = props;

    let imageTag = <></>;
    if(newsArticle.imageUrl.length > 0)
        imageTag = <img src={newsArticle.imageUrl} alt="" width={280} height={168}/>;

    return (
        <div className="news-item">
            {imageTag}
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

export default NewsCard;