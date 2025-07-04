"use client";


import { useState } from "react";
import { ContactMethod, SubscriptionStatus, TokenItem } from "@/lib/types";
import createUserTelegram from "@/lib/create-user/telegram/createUserTelegram";


async function handleSubscribe(
    setSubscribeStatus: (status: SubscriptionStatus) => void,
    contactType: ContactMethod,
    // contactValue: string,
    // tokenItems: TokenItem[],
    setNextStep: (nextStep: string) => void
): Promise<void>
{
    setSubscribeStatus(SubscriptionStatus.Loading);
    // let userID = "";
    // let userContactID = "";
    try {
        if (contactType !== ContactMethod.Telegram) {
            throw new Error("Bad contact method");
        }
        const user = await createUserTelegram();
        // userID = user.userID;
        // userContactID = user.userContactID;
        const linkToken = user.linkToken;
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
        contactType,
        contactValue
    }:
    {
        tokenItems: TokenItem[];
        contactType: ContactMethod;
        contactValue: string
    }
)
{
    console.log(tokenItems, contactValue)
    const [subscribeStatus, setSubscribeStatus] = useState<SubscriptionStatus>(SubscriptionStatus.Idle);
    const [nextStep, setNextStep] = useState<string>("");
    return (
        <div>
            <button onClick={() => handleSubscribe(
                setSubscribeStatus,
                contactType,
                // contactValue,
                // tokenItems,
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
