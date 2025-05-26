"use client";


import { useState } from "react";
import { v4 as uuidv4 } from "uuid";
import fetchFromDB from "@/lib/fetchFromDB";
import insertToDB from "@/lib/insertToDB";


async function fetchUserID(phoneNumber: string): Promise<string | null>
{
    const rows = await fetchFromDB(
        "user_channels",
        {
            select: "user_id",
            filters: [
                { column: "contact_type", operator: "eq", value: "phone" },
                { column: "contact_value", operator: "eq", value: phoneNumber }
            ]
        }
    ) as { user_id: string }[];
    return rows.length > 0 ? rows[0].user_id : null;
}


async function getUserID(phoneNumber: string): Promise<string>
{
    const existingUserID = await fetchUserID(phoneNumber);
    if (existingUserID) {
        return existingUserID;
    }
    const userID = uuidv4();
    await insertToDB("users", [{ user_id: userID}], "user_id");
    return userID;
}


async function handleSubmit(
    tokensAndStates: Record<string, string[]>,
    phoneNumber: string,
    setSubmitStatus: (status: "idle" | "loading" | "success" | "error") => void
)
{
    setSubmitStatus("loading");
    try {
        const userID = await getUserID(phoneNumber);
        await insertToDB(
            "user_channels",
            [{
                user_id: userID,
                contact_type: "phone",
                contact_value: phoneNumber,
                verified: false
            }],
            ["user_id", "contact_type", "contact_value"]
        );
        const [channel] = await fetchFromDB<{ id: string }>(
            "user_channels",
            {
                select: "id",
                filters: [
                    { column: "user_id", operator: "eq", value: userID },
                    { column: "contact_type", operator: "eq", value: "phone" },
                    { column: "contact_value", operator: "eq", value: phoneNumber }
                ],
                limit: 1
            }
        ) as { id: string }[];
        if (!channel) {
            throw new Error(`Error: No channel found for:\nuser_id=${userID} | contact_value=${phoneNumber}`);
        }
        const channelID = channel.id;
        for (const [token, states] of Object.entries(tokensAndStates)) {
            for (const state of states) {
                await insertToDB(
                    "user_subscriptions",
                    [{
                        user_id: userID,
                        token: token,
                        state: state,
                        channel_id: channelID
                    }],
                    ["user_id", "token", "state", "channel_id"]
                );
            }
        }
        setSubmitStatus("success");
    } catch (err) {
        setSubmitStatus("error");
        throw err;
    }
}


export default function SubmitComponent(
    {
        tokensAndStates,
        phoneNumber,
    }:
    {
        tokensAndStates: Record<string, string[]>;
        phoneNumber: string
    }
)
{
    const [
        submitStatus,
        setSubmitStatus
    ] = useState<"idle" | "loading" | "success" | "error">("idle");
    return (
        <div>
            <button onClick={() =>
                handleSubmit(
                    tokensAndStates,
                    phoneNumber,
                    setSubmitStatus
                )
            }>
                Submit
            </button>
            {submitStatus === "success" && (
                <p style={{ color: "green" }}>Subscription saved successfully ✅</p>
            )}
            {submitStatus === "error" && (
                <p style={{ color: "red" }}>Something went wrong. Please try again ❌</p>
            )}
        </div>
    );
}

