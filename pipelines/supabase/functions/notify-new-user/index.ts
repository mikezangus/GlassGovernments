import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js";


serve(async (req) => {
	const supabase = createClient(
		Deno.env.get("SUPABASE_URL")!,
		Deno.env.get("SUPABASE_SERVICE_RILE_KEY")!
	);
	const body = await req.json();
	const userID = body.user_id;
	const token = body.token;
	const state = body.state;
	const channelID = body.channel_id;
	const lastSent = body.last_sent;

	console.log("Body:", body);
	console.log("user id:", userID);
	console.log("token:", token);
	console.log("state:", state);
	console.log("channel id:", channelID);
	console.log("last sent:", lastSent);
})


/* To invoke locally:

	1. Run `supabase start` (see: https://supabase.com/docs/reference/cli/supabase-start)
	2. Make an HTTP request:

	curl -i --location --request POST 'http://127.0.0.1:54321/functions/v1/notify-new-user' \
		--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0' \
		--header 'Content-Type: application/json' \
		--data '{"name":"Functions"}'

*/
