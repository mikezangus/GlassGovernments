export const runtime = "edge";


import { NextRequest, NextResponse } from "next/server";
import { supabase } from "@/lib/supabase/server";
import { TokenItem } from "@/lib/types";


export async function POST(req: NextRequest): Promise<NextResponse>
{
    try {
        const body = await req.json();
        if (!body.telegramLinkToken) {
            throw new Error(`Request body missing Telegram link token`);
        }
        if (!body.tokenItems) {
            throw new Error(`Request body missing token items`);
        }
        const telegramLinkToken: string = body.telegramLinkToken;
        const tokenItemsRaw: TokenItem[] = body.tokenItems;
        const tokenItems = tokenItemsRaw.flatMap(
            ({ token, states }) =>
                states.map((state) =>
                    ({ token, state })
                )
        );
        const { error } = await supabase
            .from("telegram_handshakes")
            .insert([
                { link_token: telegramLinkToken },
                { token_items: tokenItems }
            ]);
        if (error) {
            throw new Error(`Error inserting to table telegram_handshakes for link_token=${telegramLinkToken}. Error: ${error.message}`);
        }
        return NextResponse.json({ status: "ok" });
    } catch (err) {
        return NextResponse.json({
            status: "error",
            message: (err as Error).message
        });
    }
}
