export const runtime = "edge";


import { NextRequest, NextResponse } from "next/server";
import handleMessage from "@/lib/telegram-webhook/handleMessage";


export async function POST(req: NextRequest): Promise<NextResponse>
{
	console.log("webhook | hit")
	try {
		const body = await req.json();
		console.log("webhook | body stored")
		if (body.message) {
			console.log("webhook | entering handleMessage")
			await handleMessage(body.message);
		}
		console.log("webhook | returning")
		return NextResponse.json({ status: "ok" });
	} catch (err) {
        console.error("Error from telegram-webook", err);
        return NextResponse.json({ status: "error handled" });
    }
}
