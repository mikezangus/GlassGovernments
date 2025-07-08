"use client";


import { useState } from "react";
import { ContactMethod, SubscriptionStatus, TokenItem } from "@/lib/types";


async function createUser(): Promise<{
    userID: string,
    linkToken: string
}>
{
    const res = await fetch(
        "/api/create-user/telegram",
        { method: "POST" }
    );
    if (!res.ok) {
        throw new Error("Failed to create user");
    }
    const { userID, linkToken } = await res.json(); 
    return { userID, linkToken };
}


async function createSubscription(
    userID: string,
    tokenItems: TokenItem[]
): Promise<void>
{
    const res = await fetch(
        "/api/create-subscription",
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ userID, tokenItems })
        }
    );
    if (!res.ok) {
        const error = await res.json();
        throw new Error(`Failed to create subscription for user_id=${userID}. Error: ${error.message}`);
    }
}


async function handleSubscribe(
    setSubscribeStatus: (status: SubscriptionStatus) => void,
    contactMethod: ContactMethod,
    tokenItems: TokenItem[],
    setNextStep: (nextStep: string) => void
): Promise<void>
{
    setSubscribeStatus(SubscriptionStatus.Loading);
    try {
        if (contactMethod !== ContactMethod.Telegram) {
            throw new Error("Bad contact method");
        }
        const { userID, linkToken } = await createUser();
        await createSubscription(userID, tokenItems)
        setNextStep(`https://t.me/glassgovernments_bot?start=${linkToken}`);
        setSubscribeStatus(SubscriptionStatus.Success);
    } catch (err) {
        setSubscribeStatus(SubscriptionStatus.Fail);
        throw err;
    }
}


export default function SubscribeComponent(
    {
        tokenItems,
        contactMethod,
    }:
    {
        tokenItems: TokenItem[];
        contactMethod: ContactMethod;
    }
)
{
    const [subscribeStatus, setSubscribeStatus] = useState<SubscriptionStatus>(SubscriptionStatus.Idle);
    const [nextStep, setNextStep] = useState<string>("");
    return (
        <div>
            <button onClick={() => handleSubscribe(
                setSubscribeStatus,
                contactMethod,
                tokenItems,
                setNextStep
            )}>
                Subscribe
            </button>
            {subscribeStatus === SubscriptionStatus.Success && (
                <>
                <p style={{ color: "green" }}>
                    Subscription saved successfully ✅
                </p>
                <button onClick={() => window.open(`${nextStep}`, "_blank")}>
                    Open Telegram
                </button>
                </>
            )}
            {subscribeStatus === SubscriptionStatus.Fail && (
                <p style={{ color: "red" }}>
                    Something went wrong. Please try again ❌
                </p>
            )}
        </div>
    );
}
