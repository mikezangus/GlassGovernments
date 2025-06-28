"use client";


import { useState } from "react";
import { ContactType, SubscribeStatus, TokenItem } from "@/lib/types";
import insertToDB from "@/lib/insertToDB";
import createUserTelegram from "@/lib/createUserTelegram";


async function handleSubscribe(
    setSubscribeStatus: (status: SubscribeStatus) => void,
    contactType: ContactType,
    contactValue: string,
    tokenItems: TokenItem[],
    setNextStep: (nextStep: string) => void
): Promise<void>
{
    setSubscribeStatus(SubscribeStatus.Loading);
    let userID = "";
    let userContactID = "";
    try {
        if (contactType === ContactType.Telegram) {
            const user = await createUserTelegram(contactValue);
            userID = user.userID;
            userContactID = user.userContactID;
            setNextStep(`https://t.me/glassgovernments_bot?start=${user.telegramToken}`);
        }
        for (const tokenItem of tokenItems) {
            for (const state of tokenItem.states) {
                await insertToDB(
                    "user_subscriptions",
                    [{
                        user_id: userID,
                        token: tokenItem.token,
                        state: state,
                        channel_id: userContactID
                    }],
                    ["user_id", "token", "state", "channel_id"]
                );
            }
        }
        setSubscribeStatus(SubscribeStatus.Success);
    } catch (err) {
        setSubscribeStatus(SubscribeStatus.Fail);
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
        contactType: ContactType;
        contactValue: string
    }
)
{
    const [subscribeStatus, setSubscribeStatus] = useState<SubscribeStatus>(SubscribeStatus.Idle);
    const [nextStep, setNextStep] = useState<string>("");
    return (
        <div>
            <button onClick={() => handleSubscribe(
                setSubscribeStatus,
                contactType,
                contactValue,
                tokenItems,
                setNextStep
            )}>
                Subscribe
            </button>
            {subscribeStatus === SubscribeStatus.Success && (
                <p style={{ color: "green" }}>
                    Subscription saved successfully ✅
                </p>

            )}
            {subscribeStatus === SubscribeStatus.Fail && (
                <p style={{ color: "red" }}>
                    Something went wrong. Please try again ❌
                </p>
            )}
            {nextStep && (nextStep)}
        </div>
    );
}
