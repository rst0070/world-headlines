
export async function getCountryCodes(): Promise<string[]>{

    let data = await fetch("https://localhost/api/country/country_codes")

    let result = await data.json()
    
    return new Promise(
            (resolve, reject) => {
                resolve(result)
            }
        );
}