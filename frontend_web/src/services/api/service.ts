import { CountryHeadline } from "@/types/CountryHeadline";

export class Service {

    private static BASE_URL = '';

    static async getCountryCodes(): Promise<string[]> {
        //const dataFilePath = "data/country_codes.json"
        //const jsonList = JSON.parse(await readFile(dataFilePath, {encoding: 'utf8'}))
    
        return new Promise(
            (resolve, reject) => {
                resolve(["br", "cn", "de", "fr", "gb", "il", "in", "jp", "kr", "lb", "pl", "ru", "tw", "us"])
            }
        )
    }

    static async getHeadlineMetadata(countryCode:string): Promise<CountryHeadline> {
        // const dataFilePath = "data/headline_metadata.json"
        //const jsonData = {"br": {"country_name": "Brasil", "last_update": "2024-11-19 03:00:02"}, "cn": {"country_name": "China", "last_update": "2024-11-19 03:00:02"}, "de": {"country_name": "German", "last_update": "2024-11-19 03:00:02"}, "fr": {"country_name": "Franch", "last_update": "2024-11-19 03:00:03"}, "gb": {"country_name": "United Kingdom", "last_update": "2024-11-19 03:00:03"}, "il": {"country_name": "Israel", "last_update": "2024-11-19 03:07:33"}, "in": {"country_name": "India", "last_update": "2024-11-19 03:07:07"}, "jp": {"country_name": "Japan", "last_update": "2024-11-19 03:05:44"}, "kr": {"country_name": "Korea", "last_update": "2024-11-19 03:06:43"}, "lb": {"country_name": "Lebanon", "last_update": "2024-11-19 03:03:58"}, "pl": {"country_name": "Poland", "last_update": "2024-11-19 03:03:29"}, "ru": {"country_name": "Russia", "last_update": "2024-11-19 03:03:03"}, "tw": {"country_name": "Taiwan", "last_update": "2024-11-19 03:03:30"}, "us": {"country_name": "United States", "last_update": "2024-11-19 03:03:46"}}
        //JSON.parse(await readFile(dataFilePath, {encoding: 'utf8'}))
    
        // const result:HeadlineMetadata = {
        //     countryCode: countryCode,
        //     countryName: jsonData[countryCode].country_name,
        //     lastUpdate: jsonData[countryCode].last_update
        // }

        const result: CountryHeadline = {
            countryCode: 'br',
            countryName: 'Brasil',
            lastUpdate: '2024-11-19 03:00:02'
        }
    
        return new Promise(
            (resolve, reject) => {
                resolve(result)
            }
        )
    }

    static async getNewsArticleList(countryCode:string) {
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

}