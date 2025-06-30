import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import sendWelcomeMessage from "../_shared/telegram/sendWelcomeMessage.ts";
import insertUserData from "../_shared/telegram/insertUserData.ts";


Deno.serve(async (req: Request) => {
	const body = await req.json();
	const chatID = body.message?.chat?.id;
	const text = body.message?.text;
	if (chatID && text && text.startsWith("/start")) {
		console.log("/start BODY:", JSON.stringify(body, null, 4));
		console.log("/start TEXT:", text);
		const [, linkToken] = text.split(" ");
		if (!linkToken) {
			console.error("No link token provided with /start");
			return new Response("Missing link token", { status: 400 });
		}
		try {
			await sendWelcomeMessage(chatID);
			await insertUserData(body.message, linkToken);
		} catch (err) {
			console.error("Failed to insert user data:", err);
      		return new Response("Internal error", { status: 500 });
		}
	}
  	return new Response("OK", { status: 200 });
});
