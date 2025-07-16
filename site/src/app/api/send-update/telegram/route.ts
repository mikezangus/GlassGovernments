import { supabase } from "@/lib/supabase/server";
import sendBillUpdateText from "./sendBillUpdateText";


export const runtime = "edge";


type NotificationsQueueRow = {
    user_id: string;
    bill_id: string;
    last_pubdate: string;
    sent_at: string | null;
}


async function fetchQueuedNotifications(): Promise<NotificationsQueueRow[]>
{
    const { data, error } = await supabase
        .from("notifications_queue")
        .select('*')
        .is("sent_at", null)
        .order("last_pubdate", { ascending: true });
    if (error) {
        throw new Error(error.message);
    }
    return data ?? [];
}


async function fetchTelegramID(userID: string): Promise<number | null>
{
    const { data, error } = await supabase
        .from("users_telegram")
        .select("telegram_id")
        .eq("user_id", userID)
        .maybeSingle();
    if (error) {
        throw new Error(`fetchTelegramChatId: ${error.message}`);
    }
    return data?.telegram_id ?? null;
}


export async function GET(): Promise<Response>
{
    const queue = await fetchQueuedNotifications();
    if (queue.length === 0) {
        return new Response("No updates to send");
    }
    for (const row of queue) {
        try {
            const telegramID = await fetchTelegramID(row.user_id);
            if (!telegramID) {
                console.warn(`No Telegram ID found for ${row.user_id}`);
                continue;
            }
            await sendBillUpdateText(telegramID, row.bill_id);
        } catch (err) {
            console.error(`Failed to process notification (user ${row.user_id}, bill ${row.bill_id}):`, err);
        }
    }
    return new Response(`Processed ${queue.length} queued notifications`);
}   