import { useEffect, useState } from "react";
import Select from "react-select";
import fetchFromDB from "@/lib/fetchFromDB";
import convertStateCodeToName from "@/lib/convertStateCodeToName";


export default function StatesComponent({
    selectedStates,
    setSelectedStates
}: {
    selectedStates: string[];
    setSelectedStates: (states: string[]) => void;
})
{
    const [states, setStates] = useState<{ value: string, label: string}[]>([]);
    useEffect(() => {
        async function fetchStates()
        {
            const rows = await fetchFromDB<{ state: string }>(
                "bill_metadata",
                { select: "state" }
            ) as { state: string }[];
            const states = Array.from(new Set(rows.map(row => row.state)));
            setStates(states.map(
                s => ({ value: s, label: convertStateCodeToName(s) })
            ));
        }
        fetchStates();
    }, []);
    return (
        <div style={{display: "flex", flexDirection: "column", color: "black"}}>
            <span>Select state(s)</span>
            <Select
                inputId="states"
                isMulti
                options={states}
                value={states.filter(
                    state => selectedStates.includes(state.value)
                )}
                onChange={(selected) =>
                    setSelectedStates(selected.map(state => state.value))
                }
            />
        </div>
    );
}
