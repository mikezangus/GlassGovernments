export const runtime = "edge";


import { NextRequest, NextResponse } from "next/server";
import { supabase } from "@/lib/supabase/server";
import { WordAndStates } from "@/types";


export async function POST(req: NextRequest): Promise<NextResponse>
{
    const tableName = "telegram_handshakes"
    try {
        const body = await req.json();
        if (!body.linkToken) {
            throw new Error(`Request body missing Telegram link token`);
        }
        if (!body.items) {
            throw new Error(`Request body missing token items`);
        }
        const linkToken: string = body.linkToken;
        const items: WordAndStates[] = body.items;
        const rows: {
            link_token: string,
            word: string,
            state: string
        }[] = [];
        for (const item of items) {
            for (const state of item.states) {
                rows.push({
                    link_token: linkToken,
                    word: item.word,
                    state
                });
            }
        }
        const { error } = await supabase
            .from(tableName)
            .insert(rows);
        if (error) {
            throw new Error(`Error inserting to table ${tableName} for link_token=${linkToken}. Error: ${error.message}`);
        }
        return NextResponse.json({ status: "ok" });
    } catch (err) {
        return NextResponse.json({
            status: "error",
            message: (err as Error).message
        });
    }
}
