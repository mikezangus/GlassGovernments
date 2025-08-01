import { v4 as uuid } from "uuid";
import { WordAndStates } from "@/types";


export default async function createHandshake(
    items: WordAndStates[]
): Promise<string>
{
    const linkToken = uuid();
    const res = await fetch(
        "/api/telegram-handshake",
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ linkToken, items })
        }
    );
    if (!res.ok) {
        const message = await res.text();
        throw new Error(`Error creating telegram subscription for linkToken=${linkToken}. Status: ${res.status}. Message: ${message}`);
    }
    return `https://t.me/glassgovernments_bot?start=${linkToken}`;
}
