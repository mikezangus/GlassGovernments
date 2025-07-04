import { TelegramMessageChat } from "../types";
import { supabase } from "../supabase";
import sendText from "./sendText";


interface Bill {
    bill_id?: string,
    token?: string,
    state?: string,
    bill_type?: string,
    bill_num?: string,
    enacted?: boolean,
    passed_lower?: boolean,
    passed_upper?: boolean,
    last_action_text?: string,
    last_action_date?: string,
    summary?: string
}


async function fetchUser(
    username: string,
    chatID: number
): Promise<{ userID: string, userContactID: string }>
{
    const { data, error } = await supabase
        .from("users_telegram")
        .select("user_id, user_contact_id")
        .eq("username", username)
        .eq("chat_id", chatID)
        .single();
     if (error) {
        throw new Error(`Error fetching user_id from table users_telegram via username=${username}, chat_id=${chatID}. Error message: ${error.message}`);
    }
    return { userID: data.user_id, userContactID: data.user_contact_id };
}


// async function fetchLastSentContact(
//     userID: string,
//     userContactID: string
// ): Promise<string | void>
// {
//     const { data, error } = await supabase
//         .from("user_contacts")
//         .select("last_sent")
//         .eq("user_id", userID)
//         .eq("user_contact_id", userContactID)
//         .single();
//     if (error) {
//         throw new Error(`Error fetching last_sent from table user_contacts via user_id=${userID}, user_contact_id=${userContactID}. Error message: ${error.message}`);
//     }
//     return data.last_sent;
// }


async function fetchSubscriptions(
    userID: string
): Promise<{ token: string, state: string, last_sent: string }[]>
{
    const { data, error } = await supabase
        .from("subscriptions")
        .select("last_sent, token, state")
        .eq("user_id", userID)
    if (error) {
        throw new Error(`Error fetching last_sent from table subscriptions via user_id=${userID}. Error message: ${error.message}`);
    }
    return data;
}


async function fetchBillIDs(
    subscriptions: { token: string, state: string }[]
): Promise<Bill[]>
{
    const laws: Bill[] = [];
    for (const subscription of subscriptions) {
        const { data, error } = await supabase
            .from("subscribed_bills")
            .select("bill_id")
            .eq("token", subscription.token)
            .eq("state", subscription.state)
        if (error) {
            throw new Error(`Error fetching bill_ids from table subscribed_bills for token=${subscription.token}, state=${subscription.state}. Message: ${error.message}`);
        }
        if (data) {
            for (const row of data) {
                laws.push({
                    bill_id: row.bill_id,
                    token: subscription.token,
                    state: subscription.state
                });
            }
        }
    }
    return laws;
}


async function fetchBillMetadata(bills: Bill[]): Promise<Bill[]>
{
    const billsWithMetadata: Bill[] = [];
    for (const bill of bills) {
        const { data, error } = await supabase
            .from("bill_metadata")
            .select("bill_type, bill_num, summary")
            .eq("bill_id", bill.bill_id)
            .maybeSingle()
        if (error) {
            throw new Error(`${error.message}`);
        }
        if (data) {
            billsWithMetadata.push({
                ...bill,
                bill_type: data.bill_type,
                bill_num: data.bill_num,
                summary: data.summary
            })
        }
    }
    return billsWithMetadata;
}


async function fetchBillActions(bills: Bill[]): Promise<Bill[]>
{
    const billsWithActions: Bill[] = [];
    for (const bill of bills) {
        const { data, error } = await supabase
            .from("bill_actions")
            .select("pubdate, enacted, passed_lower, passed_upper, last_action")
            .eq("bill_id", bill.bill_id)
            .order("pubdate", { ascending: false })
            .limit(1)
            .maybeSingle();
        if (error) {
            throw new Error(`${error.message}`);
        }
        if (data) {
            billsWithActions.push({
                ...bill,
                enacted: data.enacted,
                passed_lower: data.passed_lower,
                passed_upper: data.passed_upper,
                last_action_text: data.last_action,
                last_action_date: data.pubdate
            });
        }
    }
    return billsWithActions;
}


function writeBillText(bill: Bill): string
{
    const l1 = `${bill.state} ${bill.bill_type} ${bill.bill_num}`;
    // const l2 = bill.summary;
    const l3 = `Passed House: ${bill.passed_lower ? '✅' : '❌'}`;
    const l4 = `Passed Senate: ${bill.passed_upper ? '✅' : '❌'}`;
    const l5 = `Made law: ${bill.enacted ? '✅' : '❌'}`;
    const l6 = `Last action: ${bill.last_action_text} on ${bill.last_action_date?.split("T")[0] ?? ""}`
    return [l1, l3, l4, l5, l6].join('\n');
}


function writeTokenText(token: string, bills: Bill[]): string
{
    let text = `Updates for bills regulating ${token.toUpperCase()}:\n`;
    for (const bill of bills) {
        const billMessage = writeBillText(bill);
        text += `\n${billMessage}\n`;
    }
    return text.trim();
}


export default async function sendBillsText(chat: TelegramMessageChat): Promise<void>
{
    const username = chat.username!;
    const chatID = chat.id;
    const { userID } = await fetchUser(username, chatID);
    // const lastSentContact = await fetchLastSentContact(userID, userContactID);
    const subscriptions = await fetchSubscriptions(userID);
    let bills = await fetchBillIDs(subscriptions);
    bills = await fetchBillMetadata(bills);
    bills = await fetchBillActions(bills);
    const billsGroupedByToken: Record<string, Bill[]> = {};
    for (const bill of bills) {
        if (!bill.token) {
            continue;
        }
        if (!billsGroupedByToken[bill.token]) {
            billsGroupedByToken[bill.token] = [];
        }
        billsGroupedByToken[bill.token].push(bill);
    }
    for (const [token, bills] of Object.entries(billsGroupedByToken)) {
        const text = writeTokenText(token, bills);
        await sendText(chat.id, text);
    }
}
