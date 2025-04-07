import axios from "axios";
import dotenv from "dotenv";
import path from "path";
import handleRateLimit from "../../utils/handleRateLimit";


dotenv.config({ path: path.resolve(__dirname, "../../../.env")});
const API_KEY = process.env.CONGRESS_API_KEY;
const BATCH_SIZE = 250;


async function fetchResponse(congress: number, offset: number): Promise<any[]>
{
    try {
        const response = await axios.get(
            `https://api.congress.gov/v3/bill/${congress}`,
            {
                params: {
                    api_key: API_KEY,
                    format: "json",
                    offset: offset,
                    limit: BATCH_SIZE,
                }
            }
        )
        return response.data?.bills ?? [];
    } catch (err) {
        console.error(err);
        return [];
    }
}


async function fetchBatchedResponses(congress: number, offset: number): Promise<any[]>
{
    console.log(`Started fetching for Congress ${congress} [${offset} - ${offset + BATCH_SIZE}]`);
    try {
        const response = await handleRateLimit(
            () => fetchResponse(congress, offset),
            `Congress: ${congress} | Batch: ${offset} - ${BATCH_SIZE}`,
            10,
            429
        );
        return response ?? [];
    } catch (err) {
        console.error(err);
        return [];
    }
}


export default async function fetchFromWeb(congress: number): Promise<any[]>
{
    const bills: any[] = [];
    let offset = 0;
    while (true) {
        const responses = await fetchBatchedResponses(congress, offset);
        if (!responses || responses.length === 0) {
            break;
        }
        bills.push(...responses);
        offset += BATCH_SIZE;
    }
    console.log(`Finished fetching ${bills.length} records for Congress ${congress}`);
    return bills;
}
