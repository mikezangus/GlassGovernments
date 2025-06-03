import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js";


serve(async (req) => {
    const body = await req.json();
    const { bill_id, pubdate } = body;

    console.log("🔔 New bill_action received:", bill_id, pubdate);

    const supabase = createClient(
        Deno.env.get("SUPABASE_URL")!,
        Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
    );

    const { data: billMatch, error: billError } = await supabase
        .from("subscribed_bills")
        .select("token, state")
        .eq("bill_id", bill_id)
        .maybeSingle();

    if (billError || !billMatch) {
        console.error("❌ Failed to find token/state for bill_id", bill_id, billError);
        return new Response("bill not found", { status: 404 });
    }

    const { token, state } = billMatch;

    const { data: subs, error: subsError} = await supabase
        .from("user_subscriptions")
        .select("id, channel_id, last_sent")
        .eq("token", token)
        .eq("state", state);

    if (subsError) {
        console.error("❌ Error querying user_subscriptions", subsError);
        return new Response("error", { status: 500 });
    }

    for (const sub of subs ?? []) {
        const { data: channel, error: channelError } = await supabase
            .from("user_channels")
            .select("contact_value")
            .eq("id", sub.channel_id)
            .eq("contact_type", "telegram")
            .eq("verified", true)
            .maybeSingle()
        if (channelError || !channel) {
            continue;
        }

        const shouldSend = !sub.last_sent || new Date(pubdate) > new Date(sub.last_sent);
        if (!shouldSend) {
            continue;
        }

        const res = await fetch(
            `https://api.telegram.org/bot${Deno.env.get("TELEGRAM_BOT_TOKEN")}/sendMessage`,
            {
                method: "POST",
                headers: { "Content-Type": "applicatoin/json" },
                body: JSON.stringify({
                    chat_id: channel.contact_value,
                    text: `📣 New action on bill ${bill_id} in ${state}`,
                }),
            }
        );
        if (!res.ok) {
            console.error(`❌ Failed to send Telegram message to ${channel.contact_value}`);
        }

        await supabase
            .from("user_subscriptions")
            .update({ last_sent: pubdate })
            .eq("id", sub.id);

        return new Response("✅ Notifications sent (if any matched)")
    }
});