import { useState } from "react";
import { WordAndStates } from "@/lib/types";
import styles from "@/styles/bill-tracking/Words.module.css";


function Input(
    { createItem }:
    { createItem: (word: string) => void}
)
{   
    const placeholders = [
        "agriculture",
        "tax",
        "gasoline",
        "currency",
        "dairy",
        "liquor",
        "pollution",
        "health",
        "crypto",
        "fracking"
    ];
    function getPlaceholder(): string
    {
        return placeholders[Math.floor(Math.random() * placeholders.length)];
    }
    const [input, setInput] = useState("");
    const [placeholder, setPlaceholder] = useState(getPlaceholder());
    function handleSubmit(e: React.FormEvent): void
    {
        e.preventDefault();
        const word = input.trim().toLowerCase();
        if (word) {
            createItem(word);
            setInput("");
            setPlaceholder(getPlaceholder());
        }
    }
    return (
        <form
            className={styles.inputContainer}
            onSubmit={handleSubmit}
        >
            <input
                className={styles.inputText}
                type="text"
                value={input}
                placeholder={`example: ${placeholder}`}
                onChange={(e) => setInput(e.target.value)}
            />
            <button
                className={`${styles.button} ${styles.addButton}`}
                type="submit"
            >
                +
            </button>
        </form>
    );
}


function Entries(
    {
        item,
        deleteItem
    }:
    {
        item: WordAndStates;
        deleteItem: (item: WordAndStates) => void;
    }
)
{
    return (
        <div className={styles.displayChip}>
            <div className={styles.displayText}>
                {item.word}
            </div>
            <button
                className={`${styles.button} ${styles.deleteButton}`}
                onClick={() => deleteItem(item)}
            >
                X
            </button>
        </div>
    );
}


export default function WordsComponent(
    {
        items,
        setItems,
    }:
    {
        items: WordAndStates[];
        setItems: React.Dispatch<React.SetStateAction<WordAndStates[]>>;
    }
)
{
    function createItem(newWord: string): void
    {
        if (items.some(item => item.word === newWord)) {
            return;
        }
        const newItems: WordAndStates[] = [
            { word: newWord, states: [] },
            ...items
        ];
        setItems(newItems);
    }
    function deleteItem(itemToDelete: WordAndStates): void
    {
        const newItems = items.filter((item) =>
            item.word !== itemToDelete.word
        );
        setItems(newItems);
    }
    return (
        <>
        <Input createItem={createItem} />
        {
            items.length > 0 &&
            <div className={styles.displayContainer}>
                { items.map((wordAndStates) => (
                    <Entries
                        key={wordAndStates.word}
                        item={wordAndStates}
                        deleteItem={deleteItem}
                    />
                )) }
            </div>
        }
        </>
    );
}
