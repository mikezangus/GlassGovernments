import axios from "axios";
import "../../../config";
import handleRateLimit from "../../utils/handleRateLimit";
import log from "../../utils/log";
import { RawBill } from "../types";


const API_KEY = process.env.CONGRESS_API_KEY;
const BATCH_SIZE = 250;


async function fetchResponse(congress: number, offset: number): Promise<RawBill[]>
{
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
}


async function fetchBatchedResponses(congress: number, offset: number): Promise<RawBill[]>
{
    console.log(`Fetching for Congress ${congress} [${offset} - ${offset + BATCH_SIZE}]`);
    let response: RawBill[] = []
    try {
        response = await handleRateLimit(
            () => fetchResponse(congress, offset),
            `Congress ${congress} [${offset} - ${BATCH_SIZE}]`,
            10,
            429
        );
    } catch (err) {
        console.error(err);
        log(`${congress} ${err}`);
    }
    return response ?? [];
}


export default async function fetchFromWeb(congress: number): Promise<RawBill[]>
{
    const data: RawBill[] = [];
    let offset = 0;
    console.log("\n");
    while (true) {
        const responses = await fetchBatchedResponses(congress, offset);
        if (!responses || responses.length === 0) {
            break;
        }
        data.push(...responses);
        offset += BATCH_SIZE;
    }
    console.log(`Fetched ${data.length} records for Congress ${congress}`);
    return data;
}
