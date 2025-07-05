import type { NewsArticle } from "../types/NewsArticle";

interface NewsCardProps {
    newsArticle: NewsArticle;
}

const NewsCard: React.FC<NewsCardProps> = (props: NewsCardProps) => {
    const { newsArticle } = props;
    console.log(newsArticle);
    let imageTag = <></>;
    if(newsArticle.imageUrl !== null)
        imageTag = <img className="w-280px h-168px" src={newsArticle.imageUrl} alt="" width={280} height={168}/>;

    return (
        <div className="flex flex-row gap-4">
            {imageTag}
            <div className="flex flex-col gap-2">
                <h3><a href={newsArticle.url} target="_blank">{newsArticle.enTitle}</a></h3>
                <p className="article-publish-date">
                    {
                        new Date(newsArticle.publishDate)
                          .toLocaleDateString(
                            'en-US', 
                            {
                                year: 'numeric',
                                month: 'short',
                                day: 'numeric',
                                hour: '2-digit',
                                minute: '2-digit'
                            }
                          )
                    }
                </p>
                <p>{newsArticle.enDescription}</p>
                <ul className="sources">
                    <li><a href="#">{newsArticle.source}</a></li>
                </ul>
                <ul className="flex flex-row gap-2">
                    {newsArticle.enKeywords.map((keyword) => (
                        <li key={keyword}>{keyword}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default NewsCard;