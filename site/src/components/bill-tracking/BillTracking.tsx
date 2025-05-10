"use client";

import { useState } from "react";
import fetchFromDB from "@/lib/fetchFromDB";
import insertToDB from "@/lib/insertToDB"


interface User {
    phone_number: string;
    keywords: string[];
}


async function fetchUser(phoneNumber: string): Promise<User | null>
{
    try {
        const res = await fetchFromDB<User>(
            "users",
            {
                filters: [
                    { column: "phone_number", operator: "eq", value: phoneNumber}
                ],
                single: true
            }
        );
        return res as User;
    } catch {
        return null;
    }
}


async function updateUserKeywords(phoneNumber: string, keywords: string[])
{
    await insertToDB(
        "users",
        [{ phone_number: phoneNumber, keywords: keywords }],
        "phone_number"
    );
}


export default function BillTrackingComponent()
{
    const [phoneNumber, setPhoneNumber] = useState("");
    const [keyword, setKeyword] = useState("");
    const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
    const  handleSubmit = async () =>
    {
        if (phoneNumber.length > 20 || keyword.length > 20) {
            setStatus("error");
            return;
        }
        setStatus("loading");
        try {
            const user = await fetchUser(phoneNumber);
            if (user) {
                const keywords = user.keywords || [];
                if (!keywords.includes(keyword)) {
                    const updated = [...keywords, keyword];
                    await updateUserKeywords(phoneNumber, updated);     
                }
            } else {
                await insertToDB(
                    "users",
                    [{ phone_number: phoneNumber, keywords: [keyword]}]
                );
            }

    
            setStatus("success");
            setPhoneNumber("");
            setKeyword("");
        } catch {
            setStatus("error");
        }
    }
    return (
        <>
        <div style={{ display: "flex", flexDirection: "column", maxWidth: "50vw" }}>
            <input
                type="text"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                placeholder="Enter your phone number"
                maxLength={20}
            />
            <input
                type="text"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                placeholder="Enter keyword to track"
                maxLength={20}
            />
            <button onClick={handleSubmit}>Submit</button>
            {status === "success" && <div>Submitted successfully</div>}
            {status === "error" && <div>Submission failed</div>}
        </div>
        </>
    )
}
