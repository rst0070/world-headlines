import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import type { NewsArticle } from "../types/NewsArticle";
import { getNewsArticles } from "../services/api.news";
import NewsCard from "../components/NewsCard";

const CountryPage: React.FC = () => {
    const { countryCode } = useParams() as { countryCode: string };
    const [newsArticles, setNewsArticles] = useState<NewsArticle[]>([]);

    useEffect(() => {
        getNewsArticles(countryCode).then(articles => {
            setNewsArticles(articles)
        })
    }, [countryCode])

    return (
        <div>
            <h1>CountryPage {countryCode}</h1>
            {newsArticles.map((article) => (
                <NewsCard key={article.url} newsArticle={article} />
            ))}
        </div>
    )
}

export default CountryPage;