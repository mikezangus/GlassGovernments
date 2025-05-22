"use server";


import { db } from "@/lib/db";
import { NextResponse } from "next/server";


export async function GET()
{
    const { data, error } = await db
        .from("pa_bill_texts_cleaned")
        .select("*");
    if (error || !data) {
        return NextResponse.json({ error: "Failed to fetch data" }, { status: 500 });
    }
    return NextResponse.json(data);
}
