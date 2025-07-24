export const runtime = "edge";


import { NextRequest, NextResponse } from "next/server";
import handleMessage from "@/lib/telegram/handleMessage";


export async function POST(req: NextRequest): Promise<NextResponse>
{
	try {
		const body = await req.json();
		if (body.message) {
			await handleMessage(body.message);
		}
		return NextResponse.json({ status: "ok" });
	} catch (err) {
		console.error(err);
        return NextResponse.json({ status: "error handled" });
    }
}
