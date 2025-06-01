"use client";


import { ChangeEvent, useState } from "react";
import styles from "@/styles/LawTracking.module.css";
import { TokenItem } from "./types";
import TokenComponent from "./Token";


// const PLACEHOLDER_TEXTS = [
//     "agriculture",
//     "tax",
//     "gasoline",
//     "currency",
//     "dairy",
//     "liquor",
//     "pollution",
//     "health"
// ];



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

    function handleInputChange(e: ChangeEvent<HTMLInputElement>)
    {
        setInputToken(e.target.value);
    }

    function handleAdd()
    {
        const token = inputToken.trim();
        if (token === "") {
            return;
        }
        if (tokenItems.some(tokenItem => tokenItem.token === token)) {
            return;
        }
        setTokenItems([
            ...tokenItems,
            { token: token, states: [] }
        ]);
        setInputToken("");
    }
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
                onChange={(e) => handleInputChange(e)}
                onKeyDown={(e) => {
                    if (e.key === "Enter") {
                        e.preventDefault();
                        handleAdd();
                    }
                }}
            />
            <button
                className={styles.tokenInputAddButtonContainer}
                onClick={() => handleAdd()}
            >
                +
            </button>
        </div>
        <div className={styles.tokensContainer}>
            {tokenItems
                .filter(entry => entry.token.trim() !== "")
                .map((tokenItem) => (
                    <TokenComponent
                        key={tokenItem.token}
                        tokenEntry={tokenItem}
                        deleteToken={(tokenToDelete) => {
                            setTokenItems(tokenItems.filter(t => t.token !== tokenToDelete));
                        }}
                    />
            ))}
        </div>
        </div>
    );
}
