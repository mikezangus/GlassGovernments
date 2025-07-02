import { TelegramMessage } from "../types.ts";
import sendMessage from "./sendMessage.ts";
import insertNewUser from "./workflows/new-user/insertNewUser.ts";
import sendWelcomeMessage from "./workflows/new-user/sendWelcomeMessage.ts";


export default async function handleMessage(message: TelegramMessage)
{
    const chat = message.chat;
    const text = message.text;
    const [command, linkToken] = text?.split(' ') ?? [];
    if (command === "/start" && linkToken) {
        await sendWelcomeMessage(chat);
        await insertNewUser(linkToken, chat);
    } else if (command === "/start") {
        await sendMessage(chat.id, "Start button pressed");
    }
}
