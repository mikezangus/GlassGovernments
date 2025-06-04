"use client";


import { useState } from "react";
import { v4 as uuidv4 } from "uuid";
import { ContactType, SubscribeStatus, TokenItem } from "@/lib/types";
import fetchFromDB from "@/lib/fetchFromDB";
import insertToDB from "@/lib/insertToDB";


async function fetchUserID(
    contactType: ContactType,
    contactValue: string
): Promise<string | null>
{
    const rows = await fetchFromDB(
        "user_channels",
        {
            select: "user_id",
            filters: [
                { column: "contact_type", operator: "eq", value: contactType },
                { column: "contact_value", operator: "eq", value: contactValue }
            ]
        }
    ) as { user_id: string }[];
    return rows.length > 0 ? rows[0].user_id : null;
}


async function getUserID(
    contactType: ContactType,
    contactValue: string
): Promise<string>
{
    const existingUserID = await fetchUserID(contactType, contactValue);
    if (existingUserID) {
        return existingUserID;
    }
    const userID = uuidv4();
    await insertToDB("users", [{ user_id: userID}], "user_id");
    return userID;
}


async function handleSubscribe(
    setSubscribeStatus: (status: SubscribeStatus) => void,
    contactType: ContactType,
    contactValue: string,
    tokenItems: TokenItem[],
    setNextStep: (nextStep: string) => void
): Promise<void>
{
    setSubscribeStatus(SubscribeStatus.Loading);
    try {
        const userID = await getUserID(contactType, contactValue);
        await insertToDB(
            "user_channels",
            [{
                user_id: userID,
                contact_type: contactType,
                contact_value: contactValue,
                verified: false
            }],
            ["user_id", "contact_type", "contact_value"]
        );
        const [userChannelRow] = await fetchFromDB<{ id: string }>(
            "user_channels",
            {
                select: "id",
                filters: [
                    { column: "user_id", operator: "eq", value: userID },
                    { column: "contact_type", operator: "eq", value: contactType },
                    { column: "contact_value", operator: "eq", value: contactValue }
                ],
                limit: 1
            }
        ) as { id: string }[];
        if (!userChannelRow) {
            throw new Error(`Error: No channel found for:\nuser_id=${userID} | contact_type=${contactType} | contact_value=${contactValue}`);
        }
        const userChannelID = userChannelRow.id;
        for (const tokenItem of tokenItems) {
            for (const state of tokenItem.states) {
                await insertToDB(
                    "user_subscriptions",
                    [{
                        user_id: userID,
                        token: tokenItem.token,
                        state: state,
                        channel_id: userChannelID
                    }],
                    ["user_id", "token", "state", "channel_id"]
                );
            }
        }
        if (contactType === ContactType.Telegram) {
            const row = await fetchFromDB<{ token: string }>(
                "telegram_link_tokens",
                {
                    select: "token",
                    filters: [
                        { column: "user_id", operator: "eq", value: userID },
                        { column: "used", operator: "eq", value: false }
                    ],
                    limit: 1
                }
            );
            const token = Array.isArray(row) && row.length > 0
                ? row[0].token
                : uuidv4();
            await insertToDB(
                "telegram_link_tokens",
                [{
                    user_id: userID,
                    token: token,
                    used: false
                }]
            );
            setNextStep(`https://t.me/glassgovernments_bot?start=${token}`);
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
