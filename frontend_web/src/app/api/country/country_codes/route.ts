import { NextResponse } from "next/server";

export async function GET(request:Request){

    let data = await fetch("https://localhost/api/country/country_codes")

    console.log(data)

    return NextResponse.json(
        {
            country_codes: ['ko', 'us']
        },
        {
            status: 200
        }
    )

}