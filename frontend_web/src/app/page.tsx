import CountryDescContainer from "@/components/CountryDescContainer";

export default async function Home() {
  

  const descStr = "World Headlines delivers the latest global news directly. With the translation service, you can explore headlines from various countries without any language barriers."
  
  let result = (
    <>
      <main className="main-desc">
        <img src={"/icon.jpg"} alt="world-headlines icon" width={180} height={180}/>
        <p>{descStr}</p>
      </main>
      <CountryDescContainer />
    </>
  )

  return new Promise(
    (resolve, reject)=>{
      resolve(result)
    }
  );
}
