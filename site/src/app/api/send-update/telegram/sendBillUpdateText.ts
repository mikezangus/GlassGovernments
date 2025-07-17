import { supabase } from "@/lib/supabase/server";
import sendText from "@/lib/telegram/sendText";


interface Bill {
    billID: string,
    token?: string,
    state?: string,
    billType?: string,
    billNum?: string,
    enacted?: boolean,
    passedLower?: boolean,
    passedUpper?: boolean,
    lastActionText?: string,
    lastActionDate?: string,
    summary?: string
};


type NotificationsQueueRow = {
    user_id: string;
    bill_id: string;
    token: string;
    state: string;
    last_pubdate: string;
    sent_at: string | null;
}


async function fetchBillMetadata(bill: Bill): Promise<Bill>
{
    const { data, error } = await supabase
        .from("bill_metadata")
        .select("state, bill_type, bill_num, summary")
        .eq("bill_id", bill.billID)
        .maybeSingle()
    if (error || !data) {
        throw new Error(`${error?.message}`);
    }
    return {
        ...bill,
        state: data.state,
        billType: data.bill_type,
        billNum: data.bill_num,
        summary: data.summary
    };
}


async function fetchBillActions(bill: Bill): Promise<Bill>
{
    const { data, error } = await supabase
        .from("bill_actions")
        .select("pubdate, enacted, passed_lower, passed_upper, last_action")
        .eq("bill_id", bill.billID)
        .order("pubdate", { ascending: false })
        .limit(1)
        .maybeSingle();
    if (error || !data) {
        throw new Error(`${error?.message}`);
    }
    return {
        ...bill,
        enacted: data.enacted,
        passedLower: data.passed_lower,
        passedUpper: data.passed_upper,
        lastActionText: data.last_action,
        lastActionDate: data.pubdate
    };
}


function writeBillText(bill: Bill, notification: NotificationsQueueRow): string
{
    return [
        `🚨 Update for ${notification.token.toUpperCase()} in ${notification.state}:`,
        `${bill.state} ${bill.billType} ${bill.billNum}`,
        bill.summary,
        `Passed House: ${bill.passedLower ? '✅' : '❌'}`,
        `Passed Senate: ${bill.passedUpper ? '✅' : '❌'}`,
        `Made law: ${bill.enacted ? '✅' : '❌'}`,
        `Last action: ${bill.lastActionText} on ${bill.lastActionDate?.split("T")[0] ?? ""}`
    ].join('\n');
}


export default async function sendBillUpdateText(
    chatID: number,
    notification: NotificationsQueueRow
): Promise<void>
{
    let bill = { billID: notification.bill_id }
    bill = await fetchBillMetadata(bill);
    bill = await fetchBillActions(bill);
    await sendText(chatID, writeBillText(bill, notification));
}
