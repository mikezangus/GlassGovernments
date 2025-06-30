import sendMessage from "./sendMessage.ts";


export default async function sendWelcomeMessage(
    chatID: number | string
): Promise<void>
{
    const message = "Welcome to Glass Governments!";
    await sendMessage(chatID, message);
}
