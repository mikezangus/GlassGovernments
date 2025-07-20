"use client";


import React, { useState } from "react";

import ContactComponent from "./Contact";
import ProgressComponent from "./Progress";
import StatesComponent from "./States";
import SubscribeComponent from "./Subscribe";
import TokensComponent from "./TokenInput";
import { ContactMethod, Step, TokenItem } from "@/lib/types";

import styles from "@/styles/LawTracking.module.css";
// import TokenComponent from "./Token";
import NavComponent from "./Nav";


function CurrentStepComponent(
    {
        currentStep,
        tokenItems,
        setTokenItems,
        contactMethod,
        setContactType,
        contactValue,
        setContactValue
    }: {
        currentStep: Step;
        tokenItems: TokenItem[];
        setTokenItems: (tokens: TokenItem[]) => void;
        contactMethod: ContactMethod;
        setContactType: (contactMethod: ContactMethod) => void;
        contactValue: string;
        setContactValue: (contactValue: string) => void;
    }
)
{
    switch (currentStep) {
        case Step.Tokens:
            return <TokensComponent
                tokenItems={tokenItems}
                setTokenItems={setTokenItems}
            />;
        case Step.States:
            return <StatesComponent
                tokenItems={tokenItems}
                setTokenItems={setTokenItems}
            />;
        case Step.Contact:
            return (
                <>
                <ContactComponent
                    contactType={contactMethod}
                    setContactType={setContactType}
                    contactValue={contactValue}
                    setContactValue={setContactValue}
                />
                <SubscribeComponent
                    tokenItems={tokenItems}
                    contactMethod={contactMethod}
                />
                </>
            );
        default:
            return;
    }
}


export default function BillTrackingComponent()
{
    const [currentStep, setCurrentStep] = useState<Step>(Step.Tokens);
    const [tokenItems, setTokenItems] = useState<TokenItem[]>([{
        token: "",
        states: []
    }]);
    const [contactType, setContactType] = useState<ContactMethod>(ContactMethod.Telegram);
    const [contactValue, setContactValue] = useState<string>("");
    return (
        <div className={styles.lawTrackingContainer}>
            <div className={styles.bodyContainer}>
                <ProgressComponent
                    i={currentStep + 1}
                    len={Object.keys(Step).length / 2}
                />
                <CurrentStepComponent
                    currentStep={currentStep}
                    tokenItems={tokenItems}
                    setTokenItems={setTokenItems}
                    contactMethod={contactType}
                    setContactType={setContactType}
                    contactValue={contactValue}
                    setContactValue={setContactValue}
                />
                <NavComponent
                    currentStep={currentStep}
                    setCurrentStep={setCurrentStep}
                    tokenItems={tokenItems}
                    setTokenItems={setTokenItems}
                />
            </div>
        </div>
    );
}
