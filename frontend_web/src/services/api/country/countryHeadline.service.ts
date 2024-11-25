import { environment } from "@/environment";
import { CountryHeadline } from "@/types/CountryHeadline";


export async function getHeadlineInfo(countryCode:string): Promise<CountryHeadline> {
    
    let rawData = await fetch(`${environment.backendApiUrl}/api/country/headline_info?country_code=${countryCode}`)

    let data = await rawData.json()

    let result: CountryHeadline = {
        countryCode: data['country_code'],
        countryName: data['country_name'], 
        lastUpdate: data['last_update']
    }

    return new Promise(
        (resolve, reject) => {
            resolve(result)
        }
    )
    
}