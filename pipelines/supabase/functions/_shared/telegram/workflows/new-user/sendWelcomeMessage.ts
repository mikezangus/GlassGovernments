import { TelegramMessageChat } from "../../../types.ts";
import sendText from "../../sendText.ts";


export default async function sendWelcomeMessage(
    chat: TelegramMessageChat
): Promise<void>
{
    const text = `Welcome to Glass Governments!`;
    await sendText(chat.id, text);
}
