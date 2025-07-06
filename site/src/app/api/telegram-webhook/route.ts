export const runtime = "edge";


import { NextRequest, NextResponse } from "next/server";
import handleMessage from "@/lib/telegram-webhook/handleMessage";


export async function POST(req: NextRequest): Promise<NextResponse>
{
    const body = await req.json();
    if (body.message) {
		await handleMessage(body.message);
	}
  	return NextResponse.json({ status: "ok" });
}
