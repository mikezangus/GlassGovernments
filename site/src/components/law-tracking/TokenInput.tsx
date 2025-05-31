"use client";


import { ChangeEvent, useState } from "react";
import styles from "@/styles/LawTracking.module.css";
import { TokenItem } from "./types";
import TokenComponent from "./Token";


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


function handleInputChange(
    e: ChangeEvent<HTMLInputElement>,
    setInputToken: (value: string) => void
): void
{
    setInputToken(e.target.value);
}


function handleAdd(
    inputToken: string,
    setInputToken: (inputToken: string) => void,
    tokenItems: TokenItem[],
    setTokenItems: (tokenItems: TokenItem[]) => void
): void
{
    inputToken = inputToken.trim();
    if (inputToken === "") {
        return;
    }
    if (tokenItems.some(tokenItem => tokenItem.token === inputToken)) {
        return;
    }
    setTokenItems([
        ...tokenItems,
        { token: inputToken, states: [] }
    ]);
    setInputToken("");
}


export default function TokenInputComponent(
    {
        tokenItems,
        setTokenItems
    }:
    {
        tokenItems: TokenItem[];
        setTokenItems: (tokenItems: TokenItem[]) => void;
    }
)
{
    const [inputToken, setInputToken] = useState("");
    const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
        setInputToken(e.target.value);
    };
    return (
        <div>
        <div className={styles.headerContainer}>
            <span>What kinds of laws</span> 
            <span>do you want to track?</span>
        </div>
        <div className={styles.tokenInputContainer}>
            <input
                className={styles.tokenInput}
                type="text"
                placeholder="example: "
                value={inputToken}
                onChange={(e) => handleInputChange(e, setInputToken)}
                onKeyDown={(e) => {
                    if (e.key === "Enter") {
                        e.preventDefault();
                        handleAdd(
                            inputToken,
                            setInputToken,
                            tokenItems,
                            setTokenItems
                        );
                    }
                }}
            />
            <button
                className={styles.tokenInputAddButtonContainer}
                onClick={() => handleAdd(
                    inputToken,
                    setInputToken,
                    tokenItems,
                    setTokenItems
                )}
            >
                +
            </button>
        </div>
        <div className={styles.tokensContainer}>
            {tokenItems
                .filter(entry => entry.token.trim() !== "")
                .map((entry, index) => (
                    <TokenComponent
                        tokenEntry={entry}
                        deleteToken={(tokenToDelete) => {
                            setTokenItems(tokenItems.filter(t => t.token !== tokenToDelete));
                        }}
                    />
            ))}
        </div>
        </div>
    );
}
