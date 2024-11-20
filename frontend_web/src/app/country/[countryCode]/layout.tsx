import "./styles.css";
import Script from "next/script";


export default async function NewsLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <>
    {children}
    <Script src="/js/timeformat.js"/>
  </>;
}
