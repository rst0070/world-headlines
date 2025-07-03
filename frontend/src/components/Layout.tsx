import React from "react";
import NavBar from "./NavBar";

interface LayoutProps {
    children: React.ReactNode;
    countryCodes: string[];
}

const Layout: React.FC<LayoutProps> = (props: LayoutProps) => {
  const { children, countryCodes } = props;

  return (
    <>
      <header>
        <h1>
          <a href="/">
              World Headlines
          </a>
        </h1>
        <NavBar countryCodes={countryCodes} />
      </header>
      <section className="translator-section" id="google_translate_element"></section>
      {children}
    </>
  )
}

export default Layout;