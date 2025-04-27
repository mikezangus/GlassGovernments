import axios, { AxiosResponse } from "axios";
import "../../../../config"
import { BillMetadata } from "../types";
import handleRateLimit from "../../../utils/handleRateLimit";
import log from "../../../utils/log";
import populateFields from "./populateFields";


const API_KEY = process.env.CONGRESS_API_KEY;


const url = (congress: number, type: string, num: string): string => 
    "https://api.congress.gov/v3/bill/" +
    `${congress}/${type.toLowerCase()}/${num}/` +
    `actions?api_key=${API_KEY}&format=json&sort=updateDate+desc`;


export default async function fetchFromWeb(data: BillMetadata[]): Promise<void>
{
    let affected = 0;
    for (const [i, item] of data.entries()) {
        try {
            const response = await handleRateLimit(
                () => axios.get(
                    url(item.congress, item.type, String(item.num)),
                    { responseType: "json" }
                ),
                item.id,
                10,
                429
            ) as AxiosResponse<any>;
            const actions = response.data?.actions || [];
            const recordedVotes: any[] = actions
                .filter((action: any) => action.recordedVotes?.length > 0)
                .flatMap((action: any) => action.recordedVotes ?? []);
            console.log(`${recordedVotes.length > 0 ? '✅' : '❌'} [${i + 1}/${data.length}] ${item.id}`);
            if (recordedVotes.length > 0) {
                populateFields(item, recordedVotes);
                affected++;
            }
        } catch (err) {
            console.error(err);
            console.log(`${'⚠️'} [${i + 1}/${data.length}] ${item.id}`);
            log(`${item.id} | Error: ${err}`);
        }
    }
    console.log(`Fetched ${affected} actions for Congress ${data[0].congress}'s ${data.length} bills`);
}
