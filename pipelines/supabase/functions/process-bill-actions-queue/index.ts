import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js";

serve(async () => {
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  );

  const { data: queue, error: fetchError } = await supabase
    .from("bill_actions_queue")
    .select("id, bill_id, pubdate")
    .limit(10); // tune as needed

  if (fetchError || !queue?.length) {
    console.error("❌ Failed to fetch queue", fetchError);
    return new Response("empty or error", { status: 200 });
  }

  for (const item of queue) {
    const res = await fetch(
      `${Deno.env.get("SUPABASE_URL")!.replace(".supabase.co", ".functions.supabase.co")}/notify-users`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ bill_id: item.bill_id, pubdate: item.pubdate }),
      }
    );

    if (res.ok) {
      await supabase
        .from("bill_actions_queue")
        .delete()
        .eq("id", item.id);
    } else {
      console.error(`❌ notify-users failed for ${item.bill_id}`);
      // optionally increment retry counter here
    }
  }

  return new Response("✅ Queue processed");
});