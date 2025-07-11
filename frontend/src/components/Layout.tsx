import React from "react";
import { useLanguageContext } from "../context/LanguageContext";

interface LayoutProps {
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = (props: LayoutProps) => {
  const { children } = props;
  const languageContext = useLanguageContext();

  if (!languageContext) {
    throw new Error("LanguageContext not found");
  }

  const {language, setLanguage} = languageContext;

  const handleLanguageChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setLanguage(event.target.value);
  }

  return (
    <>
      <header 
        className="fixed top-0 left-0 right-0 opacity-100 z-10 bg-white flex flex-row min-h-12 justify-between items-center border-b border-gray-300 mb-10 px-4 md:px-10"
      >
        {/* Home page link */}
        <div>
          <a href="/" className="flex flex-row items-center">
            <img src="/favicon.ico" alt="World Headlines" className="w-6 h-6 md:w-8 md:h-8 mr-2 rounded-full" />
            <p className="text-lg md:text-xl font-bold">World Headlines</p>
          </a>
        </div>

        {/* Switch language button */}
        <div className="flex flex-row items-center text-sm">
          <select 
            className="w-24 md:w-48 h-8 md:h-10 rounded-md border border-gray-300 p-1 md:p-2 text-xs md:text-sm"
            value={language}
            onChange={handleLanguageChange}
          >
            <option value="en">EN</option>
            <option value="original">Original</option>
          </select>
        </div>

        {/* Explore by country link - hide on small screens, show on larger screens */}
        <p className="text-sm text-gray-500 hidden md:block">
          <a href="/#explore-by-country">
            Explore by Country
          </a>
        </p>
      </header>
      <main className="max-w-3xl w-full flex flex-col justify-center items-center mt-16 md:mt-12 px-4 ml-auto mr-auto">
        {children}
      </main>
      <footer className="flex flex-col justify-center items-center border-t border-gray-300 mt-10 mb-15">
        <p className="text-sm text-gray-500 mt-5">
          World Headlines provides various perspectives on the world.
        </p>
        <p className="text-sm text-gray-500 mt-5 flex flex-row">
          <a href="https://github.com/rst0070/world-headlines" target="_blank">
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M2.07102 11.3494L0.963068 10.2415L9.2017 1.98864H2.83807L2.85227 0.454545H11.8438V9.46023H10.2955L10.3097 3.09659L2.07102 11.3494Z" fill="currentColor"></path></svg>
            <p>GitHub</p>
          </a>
        </p>
      </footer>
    </>
  )
}

export default Layout;