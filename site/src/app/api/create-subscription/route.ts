export const runtime = "edge";


import { NextRequest, NextResponse } from "next/server";
import { supabase } from "@/lib/supabase/server";
import { WordAndStates } from "@/types";


export async function POST(req: NextRequest): Promise<NextResponse>
{
    try {
        const body = await req.json();
        if (!body.userID || !body.tokenItems) {
            throw new Error(`Request body missing userID or tokenItems. userID=${body?.userID}, tokenItems=${body?.tokenItems}`);
        }
        const userID: string = body.userID;
        const items: WordAndStates[] = body.tokenItems;
        const rows = items.flatMap(item =>
            item.states.map(state => ({
                user_id: userID,
                token: item.word,
                state
            }))
        );
        const { error } = await supabase
            .from("subscriptions")
            .insert(rows);
        if (error) {
            throw new Error(`Error inserting to table subscriptions for user_id=${userID}. Error: ${error.message}`);
        }
        return NextResponse.json({ status: "ok" });
    } catch (err) {
        return NextResponse.json({
            status: "error",
            message: (err as Error).message
        });
    }
}
