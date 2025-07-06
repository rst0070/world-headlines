import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import type { NewsArticle } from "../types/NewsArticle";
import { getNewsArticles } from "../services/api.news";
import NewsCard from "../components/NewsCard";
import type { CountryInfo } from "../types/Country";
import { getCountryInfo } from "../services/api.country";

const CountryPage: React.FC = () => {
    const { countryCode } = useParams() as { countryCode: string };
    const [newsArticles, setNewsArticles] = useState<NewsArticle[]>([]);
    const [countryInfo, setCountryInfo] = useState<CountryInfo | null>(null);

    useEffect(() => {
        getNewsArticles(countryCode).then(articles => {
            setNewsArticles(articles)
        })
        getCountryInfo(countryCode).then(info => {
            setCountryInfo(info)
        })
    }, [])

    return (
        <section className="max-w-5xl min-w-2xl flex flex-col justify-center items-center">
            <h1 className="text-xl font-bold text-left w-full mb-4">Headlines in {countryInfo?.countryName}</h1>
            <div className="flex flex-col gap-4 max-w-1xl">
                {newsArticles.map((article) => (
                    <NewsCard key={article.url} newsArticle={article} />
                ))}
            </div>
        </section>
    )
}

export default CountryPage;