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
        imageTag = <img className="w-full md:w-72 h-48 md:h-42 object-cover rounded-md" src={newsArticle.imageUrl} alt="" />;

    return (
        <div className="w-full max-w-4xl flex flex-col md:flex-row gap-4 shadow-md rounded-lg p-4 bg-white dark:bg-gray-800">
            {imageTag}
            <div className="flex flex-col gap-2 flex-1">
                <h3 className="text-left text-lg md:text-xl font-bold dark:text-white">
                    <a href={newsArticle.url} target="_blank">{title}</a>
                </h3>
                <p className="article-publish-date text-sm text-gray-600 dark:text-gray-400">
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
                <p className="text-sm md:text-base text-gray-700 dark:text-gray-300">{description}</p>
                <p className="text-sm text-gray-500 dark:text-gray-400">Source: {newsArticle.source}</p>
                <div className="flex flex-wrap gap-2">
                    <p className="text-sm text-gray-500 dark:text-gray-400">Keywords:</p>
                    {newsArticle.enKeywords.map((keyword) => (
                        <span key={keyword} className="text-xs bg-gray-100 px-2 py-1 rounded-full dark:bg-gray-700 dark:text-gray-300">{keyword}</span>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default NewsCard;