import { NextResponse } from "next/server";
import createUserTelegram from "@/lib/create-user/telegram/createUserTelegram";


export async function POST()
{
    try {
        const { userID, userContactID, linkToken } = await createUserTelegram();
        console.log(`Endpoint | Values returned from createUserTelegram: userID=${userID}, userContactID=${userContactID}, linkToken=${linkToken}`);
        return NextResponse.json({ userID, userContactID, linkToken });
    } catch (err) {
        return NextResponse.json(
            { error: err || "Failed to create Telegram user" },
            { status: 500 }
        );
    }
}
