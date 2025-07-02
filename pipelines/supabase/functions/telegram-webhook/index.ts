import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import handleMessage from "../_shared/telegram/handleMessage.ts";


Deno.serve(async (req: Request) => {
	const body = await req.json();
	if (body.message) {
		await handleMessage(body.message);
	}
  	return new Response("OK", { status: 200 });
});
