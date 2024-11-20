import { NextResponse } from "next/server";

export async function GET(request:Request){

    return NextResponse.json(
        {
            country_codes: ['ko', 'us']
        },
        {
            status: 200
        }
    )

}