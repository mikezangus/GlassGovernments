"use client";


import { useState } from "react";
import { SubmitStatus, WordAndStates } from "@/types";
import createHandshake from "@/utils/bill-tracking/db/telegram/createHandshake";
import styles from "@/styles/bill-tracking/Submit.module.css";


function Telegram({ items }: { items: WordAndStates[] })
{
    const [status, setStatus] = useState<SubmitStatus>(SubmitStatus.Idle);
    const [url, setURL] = useState<string>("");
    async function handleClick(): Promise<void>
    {
        if (status === SubmitStatus.Success && url) {
            window.open(url, "_blank");
            return;
        }
        try {
            setStatus(SubmitStatus.Loading);
            const newURL = await createHandshake(items);
            setURL(newURL);
            setStatus(SubmitStatus.Success);
            window.open(newURL, "_blank");
        } catch (err) {
            console.error(err);
            setStatus(SubmitStatus.Fail)
        } 
    }
    return (
        <div>
            <button
                className={`${styles.button} ${styles.telegram}`}
                disabled={status === SubmitStatus.Loading}
                onClick={() => handleClick()}
            >
                {status === SubmitStatus.Loading ? "Loading..." : "Track on Telegram"}
            </button>
            {status === SubmitStatus.Fail && (
                <p style={{ color: "red" }}>
                    Something went wrong. Please try again ❌
                </p>
            )}
        </div>
    );
}



// function SMSButton()
// {
//     return (

//     );
// }



export default function SubmitComponent({ items }: { items: WordAndStates[] })
{
    return (
        <div>
            {items.map(({ word, states }) => (
                <div key={word}>
                    {`${word} — ${states.join(", ")}`}
                </div>
            ))}
            <Telegram items={items} />
            {/* <SMSButton /> */}
        </div>
    );
}
