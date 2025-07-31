import handleLinkTokenMessage from "@/utils/bill-tracking/messaging/telegram/handleLinkTokenMessage";
import sendText from "@/utils/bill-tracking/messaging/telegram/sendText";
import sendBillsText from "@/utils/bill-tracking/messaging/telegram/sendBillsText";
import { TelegramMessage } from "@/types";


export default async function handleMessage(message: TelegramMessage)
{
    const chat = message.chat;
    const text = message.text;
    const [command, linkToken] = text?.split(' ') ?? [];
    if (command === "/start" && linkToken) {
        await handleLinkTokenMessage(chat, linkToken);
    } else if (command === "/start") {
        await sendText(chat.id, "Start button pressed");
    }
    try {
        await sendBillsText(chat);
    } catch (error) {
        throw error;
    }
}
