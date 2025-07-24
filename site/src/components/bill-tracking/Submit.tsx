"use client";


import { useState } from "react";
import { ContactMethod, SubscriptionStatus, WordAndStates } from "@/lib/types";
import createSubscription from "@/lib/create-subscription/createSubscription";
import styles from "@/styles/bill-tracking/Submit.module.css";



async function handleSubmit(
    contactMethod: ContactMethod,
    userInputItems: WordAndStates[],
    setURL: (url: string) => void,
    setSubmitStatus: (status: SubscriptionStatus) => void
): Promise<void>
{
    setSubmitStatus(SubscriptionStatus.Loading);
    try {
        await createSubscription(contactMethod, userInputItems, setURL, setSubmitStatus);
        setSubmitStatus(SubscriptionStatus.Success);
    } catch (err) {
        setSubmitStatus(SubscriptionStatus.Fail);
        throw err;
    }
}



function TelegramButton(
    {
        userInputItems,
        url,
        setURL,
        submitStatus,
        setSubmitStatus
    }: {
        userInputItems: WordAndStates[];
        url: string;
        setURL: (url: string) => void;
        submitStatus: SubscriptionStatus;
        setSubmitStatus: (status: SubscriptionStatus) => void
    }
)
{
    return (
        <div>
            <button
                className={styles.button}
                onClick={() => handleSubmit(ContactMethod.Telegram, userInputItems, setURL, setSubmitStatus)}
            >
                Track on Telegram
            </button>
            {submitStatus === SubscriptionStatus.Success && (
                <>
                <p style={{ color: "green" }}>
                    Subscription saved successfully ✅
                </p>
                <button onClick={() => window.open(`${url}`, "_blank")}>
                    Open Telegram
                </button>
                </>
            )}
            {submitStatus === SubscriptionStatus.Fail && (
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
    const [submitStatus, setSubmitStatus] = useState<SubscriptionStatus>(SubscriptionStatus.Idle);
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
                userInputItems={items}
                url={url}
                setURL={setURL}
                submitStatus={submitStatus}
                setSubmitStatus={setSubmitStatus}
            />
            {/* <SMSButton /> */}
        </div>
    );
}
