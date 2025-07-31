import { NotificationsQueueRow } from "@/types";
import { supabase } from "@/lib/supabase/server";


export default async function fetchQueuedNotifications(): Promise<NotificationsQueueRow[]>
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
