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
      <section className="max-w-5xl min-w-2xl flex flex-col justify-center items-center">
        <h1 className="text-xl font-bold text-left w-full mb-4">Today's Global Snapshot</h1>
        <div className="grid grid-cols-1 grid-cols-2 gap-4">
          {worldSnapshot.map((article: NewsArticle) => (
            <a href={`${article.url}`} target="_blank">
              <div 
                key={article.countryCode} 
                className="relative group max-w-72 h-48 bg-cover bg-center flex flex-col justify-center items-center"
                style={{ backgroundImage: `url(${article.imageUrl})` }}
              >
                  <h2 
                    className="relative text-white bg-black text-xl font-bold px-4 opacity-0 group-hover:opacity-100 hover:bg-opacity-75 transition-opacity duration-200 text-center z-10"
                  >
                    {article.enTitle}
                  </h2>
              </div>
            </a>
          ))}
        </div>
      </section>
      {/* <section>
        <h1>Trending Topics</h1>
      </section> */}
      <section id="explore-by-country" className="max-w-5xl min-w-2xl mt-10 flex flex-col justify-center items-center">
        <h1 className="text-xl font-bold text-left w-full mb-4">Explore by Country</h1>
        <ul className="flex flex-wrap gap-2">
          {countryCodes.map((countryCode: string) => (
            <li key={countryCode}>
              <Link 
                to={`/country/${countryCode}`}
                className="inline-block px-4 py-2 rounded-full text-gray-800 font-medium hover:opacity-80 transition-opacity duration-200"
                style={{ backgroundColor: '#F5F5DC' }}
              >
                {countryCode}
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </>
  )
}
export default HomePage;