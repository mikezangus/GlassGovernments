import { ContactMethod, SubscriptionStatus, TokenItem } from "@/lib/types";
import { v4 as uuid } from "uuid";


async function createSubscriptionTelegram(
    setNextStep: (url: string) => void,
    tokenItems: TokenItem[]
): Promise<void>
{
    const linkToken = uuid();
    const res = await fetch(
        "api/telegram-handshake",
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ linkToken, tokenItems })
        }
    );
    if (!res.ok) {
        const error = await res.json();
        throw new Error(`Error creating telegram subscription for linkToken=${linkToken}: ${error.message}`);
    }
    setNextStep(`https://t.me/glassgovernments_bot?start=${linkToken}`);
}


export default async function createSubscription(
    contactMethod: ContactMethod,
    tokenItems: TokenItem[],
    setNextStep: (nextStep: string) => void,
    setSubscriptionStatus: (status: SubscriptionStatus) => void
): Promise<void>
{
    setSubscriptionStatus(SubscriptionStatus.Loading);
    try {
        if (contactMethod === ContactMethod.Telegram) {
            await createSubscriptionTelegram(setNextStep, tokenItems);
        } else {
            throw new Error(`Bad contact method: ${contactMethod}`);
        }
        setSubscriptionStatus(SubscriptionStatus.Success);
    } catch (err) {
        setSubscriptionStatus(SubscriptionStatus.Fail);
        throw new Error(`Error: ${err}`)
    }
}
