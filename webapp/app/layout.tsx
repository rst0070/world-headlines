import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import GlobalData from "./app.data";
import { ReactNode } from "react";
import Script from "next/script";

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
  description: "Get the latest world headlines translated into your language. Stay updated with global news from the US, China, Europe, and more.",
};

async function getCountryList(): Promise<ReactNode[]> {

  let countryList = []

  return new Promise(
    (resolve, reject) => {
      GlobalData.country_codes.forEach(
        (value, index, array) => {
          let name:string = GlobalData.headline_map.get(value)?.country
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
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable}`}>
        <header>
            <h1>World Headlines</h1>
            <nav>
                <ul>
                  {await getCountryList()}
                </ul>
            </nav>
        </header>
        
        <div id="google_translate_element" style={{display:'none'}}></div>
        {children}
        <Script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"/>
        <Script src="/js/google_translate.js"/>
      </body>
    </html>
  );
}
