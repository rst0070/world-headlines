import type { CountryHeadline } from "../types/Country";

export async function getCountryCodes(): Promise<string[]>{
  let url = `/api/v1/country/country_codes`
  let response = await fetch(url)
  let data = (await response.json()) as {data: string[]}
  
  return data.data
}

export async function getHeadlineInfo(countryCode:string): Promise<CountryHeadline> {
    
  let rawData = await fetch(`/api/country/headline_info?country_code=${countryCode}`)

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