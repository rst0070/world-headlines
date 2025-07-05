import React from "react";

interface LayoutProps {
    children: React.ReactNode;
    countryCodes: string[];
}

const Layout: React.FC<LayoutProps> = (props: LayoutProps) => {
  const { children, countryCodes } = props;

  return (
    <>
      <header 
        className="fixed top-0 left-0 right-0 opacity-100 z-10 bg-white flex flex-row min-h-10 justify-between items-center border-b border-gray-300 mb-10"
      >
        <p>
          <a href="/" className="ml-10 flex flex-row items-center">
            <img src="/favicon.ico" alt="World Headlines" className="w-8 h-8 mr-2 rounded-full" />
            <p className="text-xl font-bold">World Headlines</p>
          </a>
        </p>
        <p className="text-sm text-gray-500 mr-10">
          <a href="/#explore-by-country">
            Explore by Country
          </a>
        </p>
      </header>
      <main className="max-w-1000px flex flex-col w-full justify-center items-center mt-10">
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