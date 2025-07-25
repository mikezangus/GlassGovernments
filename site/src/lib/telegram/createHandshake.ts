import { ContactMethod, SubmitStatus, WordAndStates } from "@/lib/types";
import { v4 as uuid } from "uuid";


export default async function createHandshake(
    contactMethod: ContactMethod,
    items: WordAndStates[],
    setURL: (nextStep: string) => void,
    setStatus: (status: SubmitStatus) => void
): Promise<void>
{
    setStatus(SubmitStatus.Loading);
    try {
        if (contactMethod !== ContactMethod.Telegram) {
            throw new Error(`Bad contact method: ${contactMethod}`);
        }
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
        setURL(`https://t.me/glassgovernments_bot?start=${linkToken}`);
        setStatus(SubmitStatus.Success);
    } catch (err) {
        setStatus(SubmitStatus.Fail);
        throw new Error(`Error: ${err}`)
    }
}
