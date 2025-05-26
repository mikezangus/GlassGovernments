import { useEffect, useState } from "react";
import convertStateCodeToName from "@/lib/convertStateCodeToName";
import fetchFromDB from "@/lib/fetchFromDB";


export default function StatesComponent(
    {
        tokens,
        tokensAndStates,
        setTokensAndStates
    }:
    {
        tokens: string[];
        tokensAndStates: Record<string, string[]>;
        setTokensAndStates: (newStates: Record<string, string[]>) => void;
    }
)
{
    const [
        fetchedStates,
        setFetchedStates
    ] = useState<{ value: string, label: string}[]>([]);
    useEffect(() => {
        async function fetchStates()
        {
            const rows = await fetchFromDB<{ state: string }>(
                "bill_metadata",
                { select: "state" }
            ) as { state: string }[];
            const fetchedStates = Array.from(
                new Set(rows.map(row => row.state))
            );
            setFetchedStates(fetchedStates.map(stateCode => ({
                value: stateCode,
                label: convertStateCodeToName(stateCode)
            })));
        }
        fetchStates();
    }, []);
    const handleCheckboxChange = (token: string, stateCode: string) => {
        const currentStates = tokensAndStates[token] || [];
        const isSelected = currentStates.includes(stateCode);
        const updatedStates = isSelected
            ? currentStates.filter(s => s !== stateCode)
            : [...currentStates, stateCode];
        setTokensAndStates({
            ...tokensAndStates,
            [token]: updatedStates,
        });
    };
    return (
        <div>
            {tokens.map((token) => (
                <div key={token}>
                <div>{token}</div>
                <div style={{ display: "flex", flexDirection: "column" }}>
                    {fetchedStates
                        .slice()
                        .sort((a, b) => a.label.localeCompare(b.label))
                        .map(({ value, label }) => (
                        <label key={value}>
                            <input
                                type="checkbox"
                                checked={tokensAndStates[token]?.includes(value) || false}
                                onChange={() => handleCheckboxChange(token, value)}
                            />
                            {label}
                        </label>
                    ))}
                </div>
                </div>
            ))}
        </div>
    );
}
