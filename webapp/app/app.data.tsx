import sqlite3 from "sqlite3";
import {Headline, NewsArticle, GlobalData} from './models';
import { resolve } from "path";

const db = new sqlite3.Database("world_headline.db")

async function getCountryNames(): Promise<string[]> {

    return new Promise((resolve, reject) => {
        let data: string[] = []
        db.all("SELECT country FROM HEADLINE", (err, rows) => {
            if(err){
                reject(err)
            }else{
                rows.forEach((v:any, i, a)=>{
                    data.push(v.country)
                    if(i == a.length - 1){
                        resolve(data)
                    }
                })
            }
        })
    })
}

async function getCountryCodes(): Promise<string[]> {

    return new Promise((resolve, reject) => {
        db.all("SELECT country_code FROM HEADLINE", (err, rows)=>{
            if(err){
                reject(err)
            }else{
                let v_list: string[] = []
                rows.forEach((v:any, i, a)=>{
                    v_list.push(v.country_code)
                    if(i == a.length - 1){
                        resolve(v_list)
                    }
                })
            }
        })
    })
}

async function getNewsArticles(country_name: string): Promise<NewsArticle[]> {
    return new Promise((res, rej)=>{
        let article_list: NewsArticle[] = []
        db.all(`
            SELECT url,country,source,title,description,image_url,publish_date,src_lang 
            FROM NEWS_ARTICLES
            WHERE country = '${country_name}'
            `, (err, rows) => {
                if(err){
                    rej(err)
                }else{
                    rows.forEach((v:any, i, a)=>{
                        article_list.push(
                            new NewsArticle(
                                v.url,v.country,v.source,
                                v.title,v.description,v.image_url,
                                v.publish_date,v.src_lang
                            )
                        )
                        if(i == a.length - 1){
                            res(article_list)
                        }
                    })
                }
            })
    })
}

async function getHeadline(country_code:string): Promise<Headline> {
    return new Promise((res, rej) => {
        db.get(`
            SELECT country, country_code, src_lang,url,last_update
            FROM HEADLINE
            WHERE country_code = '${country_code}'
            `,async (err, row:any)=>{
                if(err){
                    rej(err)
                }else{
                    let articles: NewsArticle[] = await getNewsArticles(row.country)
                    let headline: Headline = new Headline(
                        row.country, row.country_code, row.src_lang,
                        row.url, row.last_update, articles
                    )
                    
                    res(headline)
                }
            })
    })
}

async function getDataMap(): Promise<Map<string, Headline>>{
    
    let codes: string[] = await getCountryCodes()
    let map: Map<string, Headline> = new Map<string, Headline>()

    await Promise.all(codes.map(async (key) => {
        let headline: Headline = await getHeadline(key);
        map.set(key, headline);
    }));

    return map
}

let globalData: GlobalData;

export default async function getGlobalData(): Promise<GlobalData>{

    

    return new Promise(async (resolve, reject) => {
        if(globalData == undefined)
            globalData = new GlobalData(
                await getCountryNames(),
                await getCountryCodes(),
                await getDataMap(),
                "https://via.placeholder.com/150"
            )
        resolve(globalData)
    })
}