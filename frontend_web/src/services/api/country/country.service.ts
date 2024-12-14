import { environment } from "@/environment";

export async function getCountryCodes(): Promise<string[]>{
    let url = `${environment.backendApiUrl}/api/country/country_codes`
    console.log("sending request to " + url)
    let data = await fetch(url)

    let result = await data.json()
    
    return new Promise(
            (resolve, reject) => {
                resolve(result)
            }
        );
}