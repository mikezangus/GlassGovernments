import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js";


const SUCCESS_MESSAGE = "Welcome to Glass Governments! I will send you a brief on the laws you subscribed to shortly.";
const FAILURE_MESSAGE = "Failed to connect to Glass Governments. Please try again.";


async function parseReq(
	reqBody: any
): Promise<{ chatID: string, payload: string } | null>
{
	if (!reqBody) {
		return null;
	}
	const message = reqBody.message;
	if (!message) {
		return null;
	}
	const chatID = message.chat?.id;
	const payload = message?.text?.split(" ")[1];
	if (!chatID || !payload) {
		return null;
	}
	return { chatID, payload };
}


async function fetchTelegramLinkToken(
	userID: string,
	token: string
): Promise<string>
{
	const supabase = createClient(
		Deno.env.get("SUPABASE_URL")!,
		Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
	);
	const row = await supabase
		.from("telegram_link_tokens")
		.select("user_id, used")
		.eq("token", token)
		.maybeSingle();
	
}

async function sendTelegramMessage(
	botToken: string,
	chatID: string,
	message: string
): Promise<void>
{
	await fetch(
		`https://api.telegram.org/bot${botToken}/sendMessage`,
		{
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ chat_id: chatId, text: message }),
		}
	);
}





Deno.serve(async (req: Request) => {
	const parsedReq = await parsedReq(await req.json());
	if (!parsedReq) {
		//
	}
	const { chatID, payload } = parsedReq;
	
	const telegram_bot_token = Deno.env.get("TELEGRAM_BOT_TOKEN")!;
	
});
