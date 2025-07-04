import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import type { NewsArticle } from "../types/NewsArticle";
import { getWorldSnapshot } from "../services/api.news";

interface HomePageProps {
  countryCodes: string[];
}

const HomePage: React.FC<HomePageProps> = (props: HomePageProps) => {
  const { countryCodes } = props;

  const [worldSnapshot, setWorldSnapshot] = useState<NewsArticle[]>([]);

  useEffect(() => {
    getWorldSnapshot().then(setWorldSnapshot);
  }, []);

  return (
    <>
      <section className="ml-auto mr-auto max-w-7xl min-w-2xl">
        <h1 className="text-2xl font-bold text-center">Today's Global Snapshot</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {worldSnapshot.map((article: NewsArticle) => (
            <div key={article.countryCode}>
              <h2>{article.title}</h2>
              <img src={article.imageUrl} alt={article.title} />
            </div>
          ))}
        </div>
      </section>
      <section>
        <h1>Trending Topics</h1>
      </section>
      <section>
        <h1>Explore by Country</h1>
        <ul>
          {countryCodes.map((countryCode: string) => (
            <li key={countryCode}>
              <Link to={`/country/${countryCode}`}>{countryCode}</Link>
            </li>
          ))}
        </ul>
      </section>
    </>
  )
}
export default HomePage;