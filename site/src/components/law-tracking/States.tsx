import { useEffect, useState } from "react";
import convertStateCodeToName from "@/lib/convertStateCodeToName";
import { supabase } from "@/lib/supabase/client";
import { TokenItem } from "@/lib/types";


async function fetchStates(
    setStates: React.Dispatch<React.SetStateAction<{ 
        code: string;
        name: string;
    }[]>>
)
{
    const { data, error } = await supabase
        .from("bill_metadata")
        .select("state");
    if (error) {
        throw new Error(`Failed to fetch states from table bill_metadata. Error: ${error.message}`);
    }
    if (!data) {
        throw new Error(`No data for states fetched from table bill_metadata`);
    }
    const states = Array.from(new Set(data.map(row => row.state)));
    setStates(states.map(stateCode => ({
        code: stateCode,
        name: convertStateCodeToName(stateCode)
    })));
}


function handleChange(
    token: string,
    stateCode: string,
    tokenItems: TokenItem[],
    setTokenItems: (tokenItems: TokenItem[]) => void
)
{
    const changedTokenItems = tokenItems.map(tokenItem => {
        if (tokenItem.token !== token) {
            return tokenItem;
        }
        const selectedStates = tokenItem.states.includes(stateCode);
        const changedStates = selectedStates
            ? tokenItem.states.filter(code => code !== stateCode)
            : [...tokenItem.states, stateCode];
        return { ...tokenItem, states: changedStates };
    });
    setTokenItems(changedTokenItems);
}


export default function StatesComponent(
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
    const [states, setStates] = useState<{
        code: string,
        name: string
    }[]>([]);
    useEffect(() => {
        fetchStates(setStates)
    }, []);
    return (
        <div>
            {tokenItems.map((tokenItem) => (
                <div key={tokenItem.token}>
                    <div>{tokenItem.token}</div>
                    <div style={{ display: "flex", flexDirection: "column" }}>
                        {states
                            .slice()
                            .sort((a, b) => a.name.localeCompare(b.name))
                            .map(({ code, name }) => (
                                <label key={code}>
                                    <input
                                        type="checkbox"
                                        checked={tokenItem.states.includes(code)}
                                        onChange={() => handleChange(
                                            tokenItem.token,
                                            code,
                                            tokenItems,
                                            setTokenItems
                                        )}
                                    />
                                    {name}
                                </label>
                            ))
                        }
                    </div>
                </div>
            ))}
        </div>
    );
}
