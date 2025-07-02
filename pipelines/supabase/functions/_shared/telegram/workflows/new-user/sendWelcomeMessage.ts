import { TelegramMessageChat } from "../../../types.ts";
import sendMessage from "../../sendMessage.ts";


export default async function sendWelcomeMessage(
    chat: TelegramMessageChat
): Promise<void>
{
    const text = `Welcome to Glass Governments!`;
    await sendMessage(chat.id, text);
}
