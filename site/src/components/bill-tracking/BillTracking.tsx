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

export default async function BillTrackingComponent()
{
    const currencyBills = await fetchBillsByToken("currency");
    const agricultureBills = await fetchBillsByToken("agriculture");
    const healthcareBills = await fetchBillsByToken("healthcare");
    return (
        <div style={{ display: "flex", flexDirection: "row", gap: "5rem" }}>
            <div style={{ display: "flex", flexDirection: "column" }}>
                <div>Currency</div>
                <ul style={{ display: "flex", flexDirection: "column", margin: 0, listStyle: "none" }}>
                    {Array.isArray(currencyBills) && currencyBills.map((bill: BillMetadata) => (
                        <li key={bill.id}>{bill.bill_type} {bill.bill_num}</li>
                    ))}
                </ul>
            </div>
            <div style={{ display: "flex", flexDirection: "column" }}>
                <div>Agriculture</div>
                <ul style={{ display: "flex", flexDirection: "column", margin: 0, listStyle: "none" }}>
                    {Array.isArray(agricultureBills) && agricultureBills.map((bill: BillMetadata) => (
                        <li key={bill.id}>{bill.bill_type} {bill.bill_num}</li>
                    ))}
                </ul>
            </div>
            <div style={{ display: "flex", flexDirection: "column" }}>
                <div>Healthcare</div>
                <ul style={{ display: "flex", flexDirection: "column", margin: 0, listStyle: "none" }}>
                    {Array.isArray(healthcareBills) && healthcareBills.map((bill: BillMetadata) => (
                        <li key={bill.id}>{bill.bill_type} {bill.bill_num}</li>
                    ))}
                </ul>
            </div>
        </div>
    )
}
