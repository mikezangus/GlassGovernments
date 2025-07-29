import BillTrackingComponent from "@/components/bill-tracking/BillTracking";
import styles from "@/styles/bill-tracking/BillTracking.module.css";


async function fetchStates(): Promise<string[]>
{
    const res = await fetch(
        `https://glassgovernments.com/api/states`,
        { next: { revalidate: 3600 } }
    );
    if (!res.ok) {
        throw new Error("Failed to fetch states");
    }
    const json = await res.json();
    return json.states as string[];
}


export default async function BillTrackingPage()
{
    const states = await fetchStates();
    return (
        <div className={styles.background}>
            <div className={styles.container}>
                <BillTrackingComponent states={states}/>
            </div>
        </div>
    );
}
