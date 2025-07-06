import { useLanguageContext } from "../context/LanguageContext";
import type { NewsArticle } from "../types/NewsArticle";

interface NewsCardProps {
    newsArticle: NewsArticle;
}

const NewsCard: React.FC<NewsCardProps> = (props: NewsCardProps) => {
    const { newsArticle } = props;
    const languageContext = useLanguageContext();

    if (!languageContext) {
        throw new Error("LanguageContext not found");
    }

    const { language } = languageContext;

    let title = newsArticle.enTitle;
    let description = newsArticle.enDescription;
    if(language === "original") {
        title = newsArticle.title;
        description = newsArticle.description;
    }

    let imageTag = <></>;
    if(newsArticle.imageUrl !== null)
        imageTag = <img className="w-280px h-168px m-auto" src={newsArticle.imageUrl} alt="" width={280} height={168}/>;

    return (
        <div className="flex flex-row gap-4 shadow-md">
            {imageTag}
            <div className="flex flex-col gap-2">
                <h3 className="text-left text-lg font-bold">
                    <a href={newsArticle.url} target="_blank">{title}</a>
                </h3>
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
                <p>{description}</p>
                <ul className="sources">
                    <li><a href="#">{newsArticle.source}</a></li>
                </ul>
                <ul className="flex flex-row gap-2">
                    <p className="text-sm text-gray-500">Keywords:</p>
                    {newsArticle.enKeywords.map((keyword) => (
                        <li key={keyword}>{keyword}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default NewsCard;