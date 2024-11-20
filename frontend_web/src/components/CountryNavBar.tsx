import { ReactNode } from "react";
import { getCountryCodes, getHeadlineInfo } from "@/services/api/country";

function CountryName({countryCode, countryName} : {countryCode:string, countryName:string}){
    return (
        <li key={countryCode}>
            <a href={'/country/'+countryCode}>
                {countryName}
            </a>
        </li>
    );
}
  
async function CountryNameContainer({countryCodes}: {countryCodes:string[]}){

    let elements:ReactNode[] = []

    await Promise.all(
        countryCodes.map(
            async (val, idx, arr) => {
                let {countryCode, countryName} = await getHeadlineInfo(val);
                elements.push(
                    <CountryName
                        countryCode={countryCode}
                        countryName={countryName}
                    />
                )
            }
        )
    )

    return (
        <ul>
            {elements}
        </ul>
    );
}


export default async function CountryNavBar(){

    let countryCodes = await getCountryCodes();

    return (
        <nav>
            <CountryNameContainer countryCodes={countryCodes}/>
        </nav>
    );
}