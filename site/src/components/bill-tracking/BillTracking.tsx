"use client";

import { useState } from "react";
import fetchFromDB from "@/lib/fetchFromDB"


type BillMetadata = {
    id?: string;
    year?: number;
    session?: string;
    bill_type?: string;
    bill_num?: number;
    print_num?: number;
}


async function fetchBillsByToken(token: string): Promise<BillMetadata[]>
{
    const fetchedIDs = await fetchFromDB<{ id: string }>(
        "pa_bill_texts_cleaned",
        {
            filters: [{
                column: "tokens",
                operator: "cs",
                value: `{${token.toLowerCase()}}`
            }]
        }
    );
    const tokenIDs = Array.isArray(fetchedIDs) ? fetchedIDs : [];
    const ids = (tokenIDs ?? []).map(row => row.id);
    if (ids.length == 0) {
        return [];
    }
    const metadata = await fetchFromDB<BillMetadata>(
        "pa_bill_metadata",
        {
            filters: [{
                column: "id",
                operator: "in",
                value: `(${ids.map(id => `"${id}"`).join(",")})`
            }],
        }
    )
    return Array.isArray(metadata) ? metadata : [];
}


async function fetchBillText(id: string): Promise<string | null>
{
    const fetchedText = await fetchFromDB<{ text: string | null }>(
        "pa_bill_texts_source",
        {
            filters: [{
                column: "id",
                operator: "eq",
                value: id
            }]
        }
    );
    const text = Array.isArray(fetchedText) ? fetchedText[0] : fetchedText;
    return text?.text ?? null;
}


export default function BillTrackingComponent()
{
    const [selectedText, setSelectedText] = useState<string | null>(null);
    const [isPopupOpen, setIsPopupOpen] = useState(false);

    const [currencyBills, setCurrencyBills] = useState<BillMetadata[]>([]);
    const [agricultureBills, setAgricultureBills] = useState<BillMetadata[]>([]);
    const [healthcareBills, setHealthcareBills] = useState<BillMetadata[]>([]);

    useState(() => {
        (async () => {
            setCurrencyBills(await fetchBillsByToken("currency"));
            setAgricultureBills(await fetchBillsByToken("agriculture"));
            setHealthcareBills(await fetchBillsByToken("healthcare"));
        })();
    });

    const handleClick = async (id?: string) => {
        if (!id) {
            return;
        }
        const text = await fetchBillText(id);
        setSelectedText(text);
        setIsPopupOpen(true);
    }

    return (
        <>
            <div style={{ display: "flex", flexDirection: "row", gap: "5rem" }}>
                <div style={{ display: "flex", flexDirection: "column" }}>
                    <div>Currency</div>
                    <ul style={{ display: "flex", flexDirection: "column", margin: 0, paddingLeft: 0, listStyle: "none" }}>
                        {Array.isArray(currencyBills) && currencyBills.map((bill: BillMetadata) => (
                            <li
                                key={bill.id}
                                onClick={() => handleClick(bill.id)}
                                style={{ cursor: "pointer", textDecoration: "underline" }}
                            >
                                {bill.bill_type} {bill.bill_num}
                            </li>
                        ))}
                    </ul>
                </div>
                <div style={{ display: "flex", flexDirection: "column" }}>
                    <div>Agriculture</div>
                    <ul style={{ display: "flex", flexDirection: "column", margin: 0, paddingLeft: 0, listStyle: "none" }}>
                        {Array.isArray(agricultureBills) && agricultureBills.map((bill: BillMetadata) => (
                            <li
                                key={bill.id}
                                onClick={() => handleClick(bill.id)}
                                style={{ cursor: "pointer", textDecoration: "underline" }}
                            >
                                {bill.bill_type} {bill.bill_num}
                            </li>
                        ))}
                    </ul>
                </div>
                <div style={{ display: "flex", flexDirection: "column" }}>
                    <div>Healthcare</div>
                    <ul style={{ display: "flex", flexDirection: "column", margin: 0, paddingLeft: 0, listStyle: "none" }}>
                        {Array.isArray(healthcareBills) && healthcareBills.map((bill: BillMetadata) => (
                            <li
                                key={bill.id}
                                onClick={() => handleClick(bill.id)}
                                style={{ cursor: "pointer", textDecoration: "underline" }}
                            >
                                {bill.bill_type} {bill.bill_num}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
            {isPopupOpen && (
                <div style={{
                    position: "fixed",
                    top: "10%",
                    left: "10%",
                    width: "80%",
                    height: "80%",
                    backgroundColor: "lightgray",
                    color: "black",
                    padding: "2rem",
                    overflowY: "scroll",
                    zIndex: 1000
                }}>
                    <button onClick={() => setIsPopupOpen(false)}>Close</button>
                    <pre style={{ whiteSpace: "pre-wrap" }}>{selectedText}</pre>
                </div>
            )}
        </>

    )
}
