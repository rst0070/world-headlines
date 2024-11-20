import { ReactNode } from "react";
import { Service } from "@/services/api/service";

function getCountryDescElement(countryCode:string, countryName:string):ReactNode {

  let flag_src = "/flags/"+countryCode.toLowerCase()+".svg"
  let flag_alt = "link for "+countryName+"'s headline"
  return (
    <div className="country-desc" key={"desc-element-"+countryCode}>
      <a href={"/"+countryCode}>
        <img src={flag_src} alt={flag_alt} width={180} height={135}/>
        <p>Click to catch up latest headline news from {countryName}</p>
      </a>
    </div>
  )
}

export default async function Home() {
  
  const countryCodes = await Service.getCountryCodes()

  let countryDescElements: ReactNode[] = []
  
  await Promise.all(countryCodes.map(
    async (val, idx, arr) => {
      const headlineMetadata = await Service.getHeadlineMetadata(val)
      const element = getCountryDescElement(headlineMetadata.countryCode, headlineMetadata.countryName)
      countryDescElements.push(element)
    }
  ))

  const descStr = "World Headlines delivers the latest global news directly. With the translation service, you can explore headlines from various countries without any language barriers."
  
  let result = (
    <>
      <main className="main-desc">
        <img src={"/icon.jpg"} alt="world-headlines icon" width={180} height={180}/>
        <p>{descStr}</p>
      </main>
      <section className="country-desc-container">
        {countryDescElements}
      </section>
    </>
  )

  return new Promise(
    (resolve, reject)=>{
      resolve(result)
    }
  );
}
