"use client";


import { useState } from "react";

import ContactComponent from "./Contact";
import ProgressComponent from "./Progress";
import StatesComponent from "./States";
import SubmitComponent from "./Submit";
import TokensComponent from "./Tokens";


import styles from "@/styles/LawTracking.module.css";


enum Step {
    Tokens,
    States,
    Contact
}


export default function LawTrackingComponent()
{
    const [
        currentStep,
        setCurrentStep
    ] = useState<Step>(Step.Tokens);
    const [
        tokens,
        setTokens
    ] = useState<string[]>([""]);
    const [
        tokensAndStates,
        setTokensAndStates
    ] = useState<Record<string, string[]>>({})
    const [
        phoneNumber,
        setPhoneNumber
    ] = useState<string>("");
    const renderCurrentStep = () => {
        switch (currentStep) {
            case Step.Tokens:
                return <TokensComponent
                    tokens={tokens}
                    setTokens={setTokens}
                />;
            case Step.States:
                return <StatesComponent
                    tokens={tokens}
                    tokensAndStates={tokensAndStates}
                    setTokensAndStates={setTokensAndStates}
                />;
            case Step.Contact:
                return (
                    <div>
                    <ContactComponent
                        phoneNumber={phoneNumber}
                        setPhoneNumber={setPhoneNumber}
                    />
                    <SubmitComponent
                        tokensAndStates={tokensAndStates}
                        phoneNumber={phoneNumber}
                    />
                    </div>
                );

            default:
                return;
        }
    };
    const handleNext = () => {
        if (currentStep === Step.Tokens) {
            const filteredTokens = tokens.filter(t => t.trim() !== "");
            setTokens(filteredTokens);
        }
        if (currentStep < Step.Contact) {
            setCurrentStep(currentStep + 1);
        }
    };
    const handlePrevious = () => {
        if (currentStep > Step.Tokens) {
            setCurrentStep(currentStep - 1);
        }
    };
    return (
        <div className={styles.lawTrackingContainer}>
            <div className={styles.bodyContainer}>
                <div className={styles.progressBarContainer}>
                    <ProgressComponent
                        i={currentStep + 1}
                        len={Object.keys(Step).length / 2}
                    />
                </div>
                {renderCurrentStep()}
                <div className={styles.navigationButtons}>
                    <button
                        onClick={handlePrevious}
                        disabled={currentStep === Step.Tokens}
                        className={styles.navButton}
                    >
                        {"<-"}
                    </button>
                    <button
                        onClick={handleNext}
                        disabled={currentStep === Step.Contact}
                        className={styles.navButton}
                    >
                        {"->"}
                    </button>
                </div>
            </div>
        </div>
    );
}
