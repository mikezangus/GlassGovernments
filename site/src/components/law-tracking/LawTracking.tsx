"use client";


import { useState } from "react";

import ContactComponent from "./Contact";
import ProgressComponent from "./Progress";
import StatesComponent from "./States";
import SubmitComponent from "./Submit";
import TokensComponent from "./TokenInput";
import { Step, TokenItem } from "./types";

import styles from "@/styles/LawTracking.module.css";
import TokenComponent from "./Token";
import NavComponent from "./Nav";


function renderCurrentStep(
    currentStep: Step,
    tokenItems: TokenItem[],
    setTokenItems: (tokens: TokenItem[]) => void,
    contact: string,
    setContact: (contact: string) => void
): JSX.Element | undefined
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
                    contact={contact}
                    setContact={setContact}
                />
                <SubmitComponent
                    tokenItems={tokenItems}
                    phoneNumber={contact}
                />
                </>
            );
        default:
            return;
    }
}


export default function LawTrackingComponent()
{
    const [currentStep, setCurrentStep] = useState<Step>(Step.Tokens);
    const [tokens, setTokenItems] = useState<TokenItem[]>([{
        token: "",
        states: []
    }]);
    const [contact, setContact] = useState<string>("");
    return (
        <div className={styles.lawTrackingContainer}>
            <div className={styles.bodyContainer}>
                <ProgressComponent
                    i={currentStep + 1}
                    len={Object.keys(Step).length / 2}
                />
                {renderCurrentStep(
                    currentStep,
                    tokens,
                    setTokenItems,
                    contact,
                    setContact
                )}
                <NavComponent
                    currentStep={currentStep}
                    setCurrentStep={setCurrentStep}
                    tokenItems={tokens}
                    setTokenItems={setTokenItems}
                />
            </div>
        </div>
    );
}
