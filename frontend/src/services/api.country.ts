import type { CountryInfo } from "../types/Country";

type CountryInfoResponse = {
  country_code: string;
  country_name: string;
  last_update: string;
}

export async function getCountryCodes(): Promise<string[]>{
  let url = `/api/v1/country/country_codes`
  let response = await fetch(url)
  let data = (await response.json()) as {data: string[]}
  
  return data.data
}

export async function getCountryInfo(countryCode:string): Promise<CountryInfo> {
  let url = `/api/v1/country/country_info?country_code=${countryCode}`
  let response = await fetch(url)
  let data = (await response.json()) as {data: CountryInfoResponse}

  let result: CountryInfo = {
    countryCode: data.data.country_code,
    countryName: data.data.country_name,
    lastUpdate: data.data.last_update
  }
  
  return result
}
