export default async function sendText(
    chatID: number,
    text: string
): Promise<void>
{
    console.log("Sending text to: ", chatID)
    console.log("Text to send: ", text)
    const telegramBotToken = process.env.TELEGRAM_BOT_TOKEN;
    const url = `https://api.telegram.org/bot${telegramBotToken}/sendMessage`;
    try {
        await fetch(
            url,
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ chat_id: chatID, text })
            }
        );
    } catch (err) {
        throw new Error(`Error sending message to ${chatID}: ${err}`);
    }
}
