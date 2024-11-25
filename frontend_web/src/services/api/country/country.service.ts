import { environment } from "@/environment";

export async function getCountryCodes(): Promise<string[]>{

    let data = await fetch(`${environment.backendApiUrl}/api/country/country_codes`)

    let result = await data.json()
    
    return new Promise(
            (resolve, reject) => {
                resolve(result)
            }
        );
}