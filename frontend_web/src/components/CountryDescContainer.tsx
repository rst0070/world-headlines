import { ReactNode } from "react";
import { getCountryCodes, getHeadlineInfo } from "@/services/api/country";


function CountryDesc( 
            {countryCode, countryName} : {countryCode:string, countryName: string}){
    let flag_src = "/flags/"+countryCode.toLowerCase()+".svg"
    let flag_alt = "link for "+countryName+"'s headline"
    
    return (
        <div className="country-desc">
            <a href={"/country/"+countryCode}>
              <img src={flag_src} alt={flag_alt} width={180} height={135}/>
              <p>Click to catch up latest headline news from {countryName}</p>
            </a>
        </div>
    );

}

export default async function CountryDescContainer(){

    const countryCodes = await getCountryCodes()
    let countryDescElements: ReactNode[] = []
  
    await Promise.all(countryCodes.map(
        async (val, idx, arr) => {
            const headlineMetadata = await getHeadlineInfo(val)
            const element = 
                <CountryDesc 
                    countryCode={headlineMetadata.countryCode} 
                    countryName={headlineMetadata.countryName} 
                    key={idx}
                />;
            countryDescElements.push(element)
        }
    ))

    return (
        <section className="country-desc-container">
            {countryDescElements}
        </section>
    );
}