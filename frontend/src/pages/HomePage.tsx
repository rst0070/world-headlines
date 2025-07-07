import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import type { NewsArticle } from "../types/NewsArticle";
import { getWorldSnapshot } from "../services/api.news";
import { useLanguageContext } from "../context/LanguageContext";

interface HomePageProps {
  countryCodes: string[];
}

const HomePage: React.FC<HomePageProps> = (props: HomePageProps) => {
  const { countryCodes } = props;
  const languageContext = useLanguageContext();

  if (!languageContext) {
    throw new Error("LanguageContext not found");
  }

  const { language } = languageContext;

  const [worldSnapshot, setWorldSnapshot] = useState<NewsArticle[]>([]);

  useEffect(() => {
    getWorldSnapshot().then(setWorldSnapshot);
  }, []);

  return (
    <>
      <section className="w-full flex flex-col justify-center items-center">
        <h1 className="text-xl md:text-2xl font-bold text-left w-full mb-4">Today's Global Snapshot</h1>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 w-full">
          {worldSnapshot.map((article: NewsArticle) => (
            <a key={article.countryCode} href={`${article.url}`} target="_blank" className="w-full">
              <div 
                className="relative group w-full h-48 md:h-64 bg-cover bg-center flex flex-col justify-center items-center rounded-lg overflow-hidden"
                style={{ backgroundImage: `url(${article.imageUrl})` }}
              >
                  <h2 
                    className="relative text-white bg-black bg-opacity-50 text-base md:text-xl font-bold px-4 py-2 opacity-0 group-hover:opacity-100 hover:bg-opacity-75 transition-opacity duration-200 text-center z-10 rounded"
                  >
                    {language === "original" ? article.title : article.enTitle}
                  </h2>
              </div>
            </a>
          ))}
        </div>
      </section>

      <section id="explore-by-country" className="w-full mt-10 flex flex-col justify-center items-center">
        <h1 className="text-xl md:text-2xl font-bold text-left w-full mb-4">Explore by Country</h1>
        <ul className="flex flex-wrap gap-2 justify-center md:justify-start">
          {countryCodes.map((countryCode: string) => (
            <li key={countryCode}>
              <Link 
                to={`/country/${countryCode}`}
                className="inline-block px-3 py-2 md:px-4 md:py-2 rounded-full text-gray-800 font-medium hover:opacity-80 transition-opacity duration-200 text-sm md:text-base"
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