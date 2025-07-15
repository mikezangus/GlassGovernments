export const runtime = "edge";


import { NextRequest, NextResponse } from "next/server";
import { supabase } from "@/lib/supabase/server";
import { TokenItem } from "@/lib/types";


export async function POST(req: NextRequest): Promise<NextResponse>
{
    try {
        const body = await req.json();
        if (!body.linkToken) {
            throw new Error(`Request body missing Telegram link token`);
        }
        if (!body.tokenItems) {
            throw new Error(`Request body missing token items`);
        }
        const linkToken: string = body.linkToken;
        const tokenItems: TokenItem[] = body.tokenItems;
        const rows: { link_token: string, token: string, state: string }[] = [];
        for (const tokenItem of tokenItems) {
            for (const state of tokenItem.states) {
                rows.push({
                    link_token: linkToken,
                    token: tokenItem.token,
                    state
                });
            }
        }
        const { error } = await supabase
            .from("telegram_handshakes")
            .insert(rows);
        if (error) {
            throw new Error(`Error inserting to table telegram_handshakes for link_token=${linkToken}. Error: ${error.message}`);
        }
        return NextResponse.json({ status: "ok" });
    } catch (err) {
        return NextResponse.json({
            status: "error",
            message: (err as Error).message
        });
    }
}
