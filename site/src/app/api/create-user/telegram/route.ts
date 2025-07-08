import { NextResponse } from "next/server";
import createUserTelegram from "@/lib/create-user/telegram/createUserTelegram";


export async function POST(): Promise<NextResponse>
{
    try {
        const { userID, linkToken } = await createUserTelegram();
        console.log(`Endpoint | Values returned from createUserTelegram: userID=${userID}, linkToken=${linkToken}`);
        return NextResponse.json({ userID, linkToken });
    } catch (err) {
        return NextResponse.json(
            { error: err || "Failed to create Telegram user" },
            { status: 500 }
        );
    }
}
