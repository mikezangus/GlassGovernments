"use client";


import React, { useState } from "react";
import NavComponent from "./Nav";
import StatesComponent from "./States";
import SubmitComponent from "./Submit";
import WordsComponent from "./Words";
import { Step, WordAndStates } from "@/types";
import styles from "@/styles/bill-tracking/BillTracking.module.css";


function Renderer(
    {
        currentStep,
        wordsAndStates,
        setWordsAndStates,
        states
    }:
    {
        currentStep: Step;
        wordsAndStates: WordAndStates[];
        setWordsAndStates: React.Dispatch<React.SetStateAction<WordAndStates[]>>;
        states: string[]
    }
)
{
    switch (currentStep) {
        case 1: return (<>
            <div className={styles.cardHeader}>
                ✏️ What kinds of bills do you want to track?
            </div>
            <WordsComponent
                items={wordsAndStates}
                setItems={setWordsAndStates}
            />
        </>);
        case 2: return(<>
            <div className={styles.cardHeader}>
                📍 In which states do you want to track these bills?
            </div>
            <StatesComponent
                items={wordsAndStates}
                setItems={setWordsAndStates}
                states={states}
            />
        </>);
        case 3: return(<>
            <div className={styles.cardHeader}>
                ✅ Your bills are ready to track
            </div>
            <SubmitComponent items={wordsAndStates} />
        </>);
        default: return(<div>whoopsies uwu</div>);
    };
}


export default function BillTrackingComponent(
    { states }:
    { states: string[] }
)
{
    const [currentStep, setCurrentStep] = useState<Step>(1);
    const [wordsAndStates, setWordsAndStates] = useState<WordAndStates[]>([]);
    return (
        <div className={styles.card}>
            <Renderer
                currentStep={currentStep}
                wordsAndStates={wordsAndStates}
                setWordsAndStates={setWordsAndStates}
                states={states}
            />
            {
                wordsAndStates.length > 0 && 
                <NavComponent
                    currentStep={currentStep}
                    setCurrentStep={setCurrentStep} 
                />
            }
        </div>
    );
}
