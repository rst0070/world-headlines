import type { MetadataRoute } from 'next'
import { getCountryCodes } from '@/services/api/country'
import { environment } from '@/environment'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {

    let countryCodes: string[] = await getCountryCodes()
    let prefix:string = environment.siteUrlPrefix

    
    let result: MetadataRoute.Sitemap = [
        {
            url: prefix,
            lastModified: new Date(),
            changeFrequency: 'yearly',
            priority: 0.8,
        }
    ]

    await Promise.all(countryCodes.map(async (val, idx, arr)=>{
        result.push(
            {
                url: prefix+"/country/"+val,
                lastModified: new Date(),
                changeFrequency: 'hourly',
                priority: 1,
            }
        )
    }))

    return new Promise((resolve, reject)=>{
        resolve(result)
    })
}