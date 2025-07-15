import { TelegramMessageChat } from "../types";
import sendText from "./sendText";


export default async function sendWelcomeMessage(
    chat: TelegramMessageChat
): Promise<void>
{
    const text = `Welcome to Glass Governments!`;
    await sendText(chat.id, text);
}
