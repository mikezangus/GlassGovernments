"use client";


import { useState } from "react";
import { ContactMethod, SubmitStatus, WordAndStates } from "@/types";
import createHandshake from "@/utils/bill-tracking/db/telegram/createHandshake";
import styles from "@/styles/bill-tracking/Submit.module.css";


function TelegramButton(
    {
        items,
        url,
        setURL,
        status,
        setStatus
    }: {
        items: WordAndStates[];
        url: string;
        setURL: (url: string) => void;
        status: SubmitStatus;
        setStatus: (status: SubmitStatus) => void
    }
)
{
    return (
        <div>
            <button
                className={styles.button}
                onClick={() =>
                    createHandshake(ContactMethod.Telegram, items, setURL, setStatus)
                }
            >
                Track on Telegram
            </button>
            {status === SubmitStatus.Success && (
                <>
                <p style={{ color: "green" }}>
                    Subscription saved successfully ✅
                </p>
                <button onClick={() => window.open(`${url}`, "_blank")}>
                    Open Telegram
                </button>
                </>
            )}
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
    const [status, setStatus] = useState<SubmitStatus>(SubmitStatus.Idle);
    const [url, setURL] = useState<string>("");
    return (
        <div>
            {items.map((item) => (
                <div key={item.word}>
                    <div>{item.word}</div>
                    {item.states!.map((state) => (
                        <div key={state}>{state}</div>
                    ))}
                </div>

            ))}
            <TelegramButton
                items={items}
                url={url}
                setURL={setURL}
                status={status}
                setStatus={setStatus}
            />
            {/* <SMSButton /> */}
        </div>
    );
}
