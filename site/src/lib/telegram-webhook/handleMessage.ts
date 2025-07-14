import { TelegramMessage } from "../types";
import sendText from "./sendText";
// import insertNewUser from "./insertNewUser";
import sendBillsText from "./sendBillsText";
// import sendWelcomeMessage from "./sendWelcomeMessage";
import handleLinkTokenMessage from "./handleLinkTokenMessage";


export default async function handleMessage(message: TelegramMessage)
{
    console.log(`handleMessage | message=${message}`)
    const chat = message.chat;
    const text = message.text;
    console.log(`handleMessage | text=${text}`);
    const [command, linkToken] = text?.split(' ') ?? [];
    if (command === "/start" && linkToken) {
        console.log(`handleMessage | linkToken=${linkToken}`)
        await sendText(chat.id, `Your link token is ${linkToken}`)
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
