import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import getGlobalData from "./app.data";
import { ReactNode } from "react";
import Script from "next/script";
import { GlobalData } from "./models";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "World Headlines - Global News in Your Language",
  description: "Check out headlines from around the world. Stay updated with global news from the US, China, Europe, and more.",
};

async function getCountryList(): Promise<ReactNode[]> {

  let countryList = []

  return new Promise(
    async (resolve, reject) => {

      let data = await getGlobalData()

      data.countryCodes.forEach(
        (value, index, array) => {
          let name = data.headlineMap.get(value)?.country
          countryList.push(
            <li key={value}><a href={'/'+value}>{name}</a></li>
          )
          if(index == array.length-1){
            resolve(countryList)
          }
        }
      )
    }
  )
}

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html>
      <body className={`${geistSans.variable} ${geistMono.variable}`}>
        <header>
            <h1><a href="/">World Headlines</a></h1>
            <nav>
                <ul>
                  {await getCountryList()}
                </ul>
            </nav>
        </header>
        <section className="translator-section" id="google_translate_element"></section>
        {children}
        <Script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"/>
        <Script src="/js/google_translate.js"/>
      </body>
    </html>
  );
}
