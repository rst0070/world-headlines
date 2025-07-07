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
        <ul className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4 w-full">
          {countryCodes.map((countryCode: string) => (
            <li key={countryCode} className="w-full">
              <Link 
                to={`/country/${countryCode}`}
                className="group relative block w-full px-4 py-4 rounded-2xl text-center font-bold text-slate-600 bg-white border-2 border-slate-200 hover:border-blue-300 hover:text-blue-600 hover:shadow-xl hover:shadow-blue-100/50 hover:-translate-y-1 hover:scale-105 transition-all duration-300 ease-out"
              >
                <span className="relative z-10 text-sm tracking-wider uppercase">
                  {countryCode}
                </span>
                
                {/* background pattern */}
                <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-blue-50/0 to-blue-50/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                
                {/* effect */}
                <div className="absolute top-0 left-0 right-0 h-1/2 rounded-t-2xl bg-gradient-to-b from-white/40 to-transparent opacity-60"></div>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </>
  )
}
export default HomePage;