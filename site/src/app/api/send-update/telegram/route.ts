export const runtime = "edge";


import fetchQueuedNotifications from "@/utils/bill-tracking/db/telegram/fetchQueuedNotifications";
import fetchTelegramID from "@/utils/bill-tracking/db/telegram/fetchTelegramID";
import sendBillUpdateText from "@/utils/bill-tracking/messaging/telegram/sendBillUpdateText";



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
            await sendBillUpdateText(telegramID, row);
        } catch (err) {
            console.error(`Failed to process notification (user ${row.user_id}, bill ${row.bill_id}):`, err);
        }
    }
    return new Response(`Processed ${queue.length} queued notifications`);
}
