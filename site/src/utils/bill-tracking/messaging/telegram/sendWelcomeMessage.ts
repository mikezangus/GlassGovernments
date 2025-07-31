import sendText from "@/utils/bill-tracking/messaging/telegram/sendText";
import { TelegramMessageChat } from "@/types";


export default async function sendWelcomeMessage(
    chat: TelegramMessageChat
): Promise<void>
{
    const text = `Welcome to Glass Governments!`;
    await sendText(chat.id, text);
}
