export const runtime = "edge";


import { NextRequest, NextResponse } from "next/server";
import { supabase } from "@/lib/supabase/server";
import { TokenItem } from "@/lib/types";


export async function POST(req: NextRequest): Promise<NextResponse>
{
    console.log("hit telegram handshake")
    try {
        const body = await req.json();
        if (!body.linkToken) {
            console.log("telegram handshake | no telegram link token")
            throw new Error(`Request body missing Telegram link token`);
        }
        if (!body.tokenItems) {
            console.log("telegram handshake | no token items")
            throw new Error(`Request body missing token items`);
        }
        const linkToken: string = body.linkToken;
        const tokenItemsRaw: TokenItem[] = body.tokenItems;
        console.log(`telegram handshake | linkToken=${linkToken}`);
        console.log(`telegram handshake | tokenItems=${tokenItemsRaw}`);
        const tokenItems = tokenItemsRaw.flatMap(
            ({ token, states }) =>
                states.map((state) =>
                    ({ token, state })
                )
        );
        const { error } = await supabase
            .from("telegram_handshakes")
            .insert({
                link_token: linkToken,
                token_items: tokenItems
            });
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
