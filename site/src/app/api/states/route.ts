export const runtime = "edge";


import { NextResponse } from "next/server";
import { supabase } from "@/lib/supabase/server";


export async function GET(): Promise<NextResponse>
{
    const tableName = "states";
    try {
        const { data, error } = await supabase
            .from(tableName)
            .select("state")
            .order("state");
        if (error) {
            throw new Error(`Error trying to fetch states from table ${tableName}: ${error.message}`);
        }
        if (!data) {
            throw new Error(`No data for states fetched from table ${tableName}`);
        }
        const states: string[] = [];
        for (const row of data) {
            states.push(row.state as string);
        }
        return NextResponse.json({ status: "ok", states });
    } catch (err) {
        return NextResponse.json(
            { status: "error", message: (err as Error).message },
            { status: 500 }
        );
    }
}
