import { TelegramMessage } from "../types.ts";
import sendText from "./sendText.ts";
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
        await sendText(chat.id, "Start button pressed");
    }
}
