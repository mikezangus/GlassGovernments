"use client";


import { useState } from "react";
import { v4 as uuidv4 } from "uuid";
import KeywordsComponent from "./Keywords";
import PhoneNumberComponent from "./PhoneNumber";
import StatesComponent from "./States";
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
    phoneNumber: string,
    keywords: string[],
    states: string[],
    setSubmitStatus: (status: "idle" | "loading" | "success" | "error") => void
)
{
    console.log("STATES:", states)
    console.log("KEYWORDS:", keywords)
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
        for (const state of states) {
            for (const keyword of keywords) {
                console.log("STATE:", state)
                console.log("KEYWORD:", keyword)
                await insertToDB(
                    "subscriptions",
                    [{
                        user_id: userID,
                        token: keyword,
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


export default function BillTrackingComponent()
{
    const [phoneNumber, setPhoneNumber] = useState("");
    const [keywords, setKeywords] = useState<string[]>([]);
    const [states, setStates] = useState<string[]>([]);
    const [submitStatus, setSubmitStatus] = useState<
        "idle" | "loading" | "success" | "error"
    >("idle");
    return (
        <div
            style={{
                display: "flex",
                flexDirection: "column",
                gap: "1rem",
                maxWidth: "400px"
            }}
        >
            <PhoneNumberComponent 
                phoneNumber={phoneNumber}
                setPhoneNumber={setPhoneNumber}
            />
            <KeywordsComponent
                keywords={keywords}
                setKeywords={setKeywords}
            />
            <StatesComponent
                selectedStates={states}
                setSelectedStates={setStates}
            />
            <button onClick={
                () => handleSubmit(
                    phoneNumber,
                    keywords,
                    states,
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
