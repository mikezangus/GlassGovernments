import { TelegramMessage } from "../types";
import sendText from "./sendText";
import insertNewUser from "./insertNewUser";
import sendBillsText from "./sendBillsText";
import sendWelcomeMessage from "./sendWelcomeMessage";


export default async function handleMessage(message: TelegramMessage)
{
    const chat = message.chat;
    const text = message.text;
    const [command, linkToken] = text?.split(' ') ?? [];
    if (command === "/start" && linkToken) {
        await sendWelcomeMessage(chat);
        await insertNewUser(linkToken, chat);
    } else if (command === "/start") {
        await sendText(chat.id, "Start button pressed");
    }
    try {
        await sendBillsText(chat);
    } catch (error) {
        throw error;
    }
    
}
