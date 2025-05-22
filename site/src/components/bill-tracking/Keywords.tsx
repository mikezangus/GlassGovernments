import { useState } from "react";


export default function KeywordsComponent({
    keywords,
    setKeywords
}: {
    keywords: string[];
    setKeywords: (kw: string[]) => void;
})
{
    const [keywordInput, setKeywordInput] = useState("");
    function handleAdd()
    {
        const trimmed = keywordInput.trim();
        if (trimmed && !keywords.includes(trimmed)) {
            setKeywords([...keywords, trimmed]);
            setKeywordInput("");
        }
    }
    function handleRemove(kw: string)
    {
        setKeywords(keywords.filter(k => k !== kw));
    }
    return (
        <div style={{display: "flex", flexDirection: "column"}}>
            <span>Keywords</span>
            <input
                type="text"
                value={keywordInput}
                onChange={(e) => setKeywordInput(e.target.value)}
                style={{
                    width: "100%",
                    padding: "0.5rem",
                    border: "1px solid #ccc",
                    borderRadius: "4px"
                }}
            />
            <button
                type="button"
                onClick={handleAdd}
                style={{
                    display: "block",
                    margin: "0.5rem auto 1rem",
                    fontSize: "1.2rem",
                    padding: "0.25rem 0.75rem",
                    borderRadius: "50%",
                    border: "1px solid #ccc",
                    background: "#f9f9f9",
                    cursor: "pointer"
                }}
            >
                +
            </button>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem", color: "black" }}>
                {keywords.map((kw, i) => (
                    <div
                        key={i}
                        style={{
                            display: "inline-flex",
                            alignItems: "center",
                            padding: "0.25rem 0.5rem",
                            background: "#e0e0e0",
                            borderRadius: "999px"
                        }}
                    >
                        <span>
                            {kw}
                        </span>
                        <button
                            onClick={() => handleRemove(kw)}
                            style={{
                                marginLeft: "0.5rem",
                                background: "none",
                                border: "none",
                                cursor: "pointer",
                                fontWeight: "bold"
                            }}
                        >
                            x
                        </button>
                    </div>
                ))}
            </div>
        </div>
    )
}
