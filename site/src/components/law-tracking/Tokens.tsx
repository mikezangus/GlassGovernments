"use client";


import { ChangeEvent, useState } from "react";
import styles from "@/styles/LawTracking.module.css";


const PLACEHOLDER_TEXTS = [
    "agriculture",
    "tax",
    "gasoline",
    "currency",
    "dairy",
    "liquor",
    "pollution",
    "health"
];


function TokenEntryComponent(
    {
        index,
        value,
        onChange,
        onBlur,
        onDelete
    }:
    {
        index: number;
        value: string;
        onChange: (index: number, newValue: string) => void;
        onBlur: (index: number) => void;
        onDelete: (index: number) => void;
    }
)
{
    const [hasBlurred, setHasBlurred] = useState(false);
    const handleBlur = () => {
        setHasBlurred(true);
        onBlur(index);
    };
    const placeholderText = PLACEHOLDER_TEXTS[index % PLACEHOLDER_TEXTS.length];
    return (
        <div className={styles.tokenEntryContainer}>
            <input
                type="text"
                placeholder={`example: ${placeholderText}`}
                className={styles.tokenInput}
                value={value}
                onChange={
                    (e: ChangeEvent<HTMLInputElement>) =>
                        onChange(index, e.target.value)
                }
                onBlur={handleBlur}
            />
            {hasBlurred && value.trim() !== "" && (
                <button
                    className={styles.deleteButton}
                    onClick={() => onDelete(index)}
                >
                    x
                </button>
            )}
        </div>

    );
}


export default function TokensComponent(
    {
        tokens,
        setTokens
    }:
    {
        tokens: string[];
        setTokens: (tokens: string[]) => void;
    }
)
{
    const handleChange = (index: number, newValue: string) => {
        const updatedTokens = [...tokens];
        updatedTokens[index] = newValue;
        setTokens(updatedTokens);
    };
    const handleBlur = (index: number) => {
        const isLast = index === tokens.length - 1;
        const notEmpty = tokens[index].trim() !== "";
        if (isLast && notEmpty) {
            setTokens([...tokens, ""]);
        }
    };
    const handleDelete = (index: number) => {
        if (tokens.length === 1 || index === 0) {
            const updated = [...tokens];
            updated[0] = "";
            setTokens(updated);
        } else {
            const updated = tokens.filter((_, i) => i !== index);
            setTokens(updated);
        }
    };
    return (
        <>
        <div className={styles.headerContainer}>
            <span>What kinds of laws</span> 
            <span>do you want to track?</span>
        </div>
        <div className={styles.tokenEntriesContainer}>
            {tokens.map((token, index) => (
                <TokenEntryComponent
                    key={index}
                    index={index}
                    value={token}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    onDelete={handleDelete}
                />
            ))}
        </div>
        </>
    );
}
