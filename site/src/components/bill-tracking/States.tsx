import { WordAndStates } from "@/types";
import convertStateCodeToName from "@/utils/convertStateCodeToName";


function DisplayItem(
    {
        item,
        setItem,
        states
    }:
    {
        item: WordAndStates,
        setItem: (item: WordAndStates) => void;
        states: string[]
    }
)
{
    function toggleStates(state: string): void
    {
        const inList = item.states?.includes(state);
        const newList = inList
            ? item.states!.filter((s) => s !== state)
            : [...(item.states ?? []), state];
        setItem({ ...item, states: newList });
    }
    return (
        <div style={{ marginBottom: "1.5rem" }}>
            <h4 style={{ margin: "0 0 .5rem" }}>{item.word}</h4>

             <div style={{ display: "flex", flexDirection: "column", gap: ".25rem" }}>
                {states.map((state) => (
                    <label key={state}>
                    <input
                        type="checkbox"
                        checked={item.states?.includes(state) ?? false}
                        onChange={() => toggleStates(state)}
                    />
                    {convertStateCodeToName(state)}
                    </label>
                ))}
            </div>
        </div>
    );
}


export default function StatesComponent(
    {
        items,
        setItems,
        states
    }:
    {
        items: WordAndStates[];
        setItems: (items: WordAndStates[]) => void;
        states: string[]
    }
)
{
    function updateItem(word: string, next: WordAndStates): void
    {
        const updated = items.map((item) =>
            item.word === word ? next : item
        );
        setItems(updated);
    }
    return (
        <div>
            {items.map((item) => (
                <DisplayItem
                    key={item.word}
                    item={item}
                    setItem={(next) => updateItem(item.word, next)}
                    states={states}
                />
            ))}
        </div>
    );
}
