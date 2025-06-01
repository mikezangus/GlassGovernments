// supabase/functions/telegram-handler/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js";

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  );

  const body = await req.json();
  const message = body?.message;
  const chatId = message?.chat?.id;
  const payload = message?.text?.split(" ")[1]; // "/start TOKEN"

  if (!chatId || !payload) {
    return new Response("OK");
  }

  const { data: tokenRow } = await supabase
    .from("telegram_link_tokens")
    .select("user_id, used")
    .eq("token", payload)
    .maybeSingle();

  if (!tokenRow || tokenRow.used) {
    await sendTelegramMessage(chatId, "❌ Invalid or expired link.");
    return new Response("OK");
  }

  await supabase.from("user_channels").insert({
    user_id: tokenRow.user_id,
    contact_type: "telegram",
    contact_value: chatId.toString(),
    verified: true,
  });

  await supabase
    .from("telegram_link_tokens")
    .update({ used: true })
    .eq("token", payload);

  await sendTelegramMessage(chatId, "✅ Telegram connected! You’ll now receive alerts.");
  return new Response("OK");
});

async function sendTelegramMessage(chatId: number, text: string) {
  const BOT_TOKEN = Deno.env.get("TELEGRAM_BOT_TOKEN")!;
  await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: chatId, text }),
  });
}