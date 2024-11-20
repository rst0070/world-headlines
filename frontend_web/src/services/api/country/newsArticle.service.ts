import { NewsArticle } from "@/types/NewsArticle";

export async function getNewsArticles(countryCode:string): Promise<NewsArticle[]>{
    
    let response = await fetch(`https://localhost/api/country/news_articles?country_code=${countryCode}`)

    let dataList = await response.json()

    let result:NewsArticle[] = []

    await Promise.all(
        dataList.map(
          (val, idx, arr) => {
              result.push({
                  countryCode: val['country_code'],
                  url: val['url'],
                  title: val['title'],
                  description: val['description'],
                  imageUrl: val['image_url'],
                  publishDate: val['publish_date'],
                  source: val['source']
              })
          }
        )
    )

    return result;


    return [{
        countryCode: "us",
        url: "https://example.com/news/1",
        title: "SpaceX Successfully Launches New Satellite Constellation",
        description: "SpaceX has successfully deployed 60 new Starlink satellites into orbit, expanding its global internet coverage network.",
        imageUrl: "https://example.com/images/spacex-launch.jpg",
        publishDate: "2024-03-15T08:30:00Z",
        source: "Tech News Daily"
      },
      {
        countryCode: "jp",
        url: "https://example.com/news/2",
        title: "Cherry Blossom Season Arrives Early in Tokyo",
        description: "Japan's iconic cherry blossoms have begun blooming earlier than expected in Tokyo, drawing crowds to popular viewing spots.",
        imageUrl: "https://example.com/images/cherry-blossoms.jpg",
        publishDate: "2024-03-14T15:45:00Z",
        source: "Japan Times"
      },
      {
        countryCode: "uk",
        url: "https://example.com/news/3",
        title: "British Museum Unveils New Ancient Egyptian Exhibition",
        description: "A groundbreaking exhibition featuring newly discovered artifacts from ancient Egypt opens this weekend at the British Museum.",
        imageUrl: "https://example.com/images/egyptian-exhibit.jpg",
        publishDate: "2024-03-14T12:15:00Z",
        source: "The Guardian"
      },
      {
        countryCode: "fr",
        url: "https://example.com/news/4",
        title: "Paris Olympics Infrastructure Nears Completion",
        description: "Final preparations are underway for the 2024 Summer Olympics as Paris completes its major infrastructure projects.",
        imageUrl: "https://example.com/images/paris-olympics.jpg",
        publishDate: "2024-03-13T16:20:00Z",
        source: "Le Monde"
      },
      {
        countryCode: "de",
        url: "https://example.com/news/5",
        title: "German Auto Industry Embraces Electric Vehicle Revolution",
        description: "Major German automakers announce ambitious plans to accelerate their transition to electric vehicle production.",
        imageUrl: "https://example.com/images/ev-production.jpg",
        publishDate: "2024-03-13T09:45:00Z",
        source: "Der Spiegel"
      }
    ];
}