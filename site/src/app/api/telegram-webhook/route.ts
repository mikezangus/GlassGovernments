export const runtime = "edge";


import { NextRequest, NextResponse } from "next/server";
import handleMessage from "@/lib/telegram-webhook/handleMessage";


export async function POST(req: NextRequest): Promise<NextResponse>
{
	console.log("WEBHOOK HIT");
    const body = await req.json();
	console.log("Body:", body);
    if (body.message) {
		console.log("Message:", body.message);
		await handleMessage(body.message);
	}
  	return NextResponse.json({ status: "ok" });
}
