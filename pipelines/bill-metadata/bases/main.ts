import { Bill } from "../types";
import fetchFromWeb from "./fetchFromWeb";
import insertToDB from "./insertToDB";
import process from "./process";


const START_CONGRESS = 102;
const END_CONGRESS = 102;


async function main()
{
    const data: Bill[] = []
    for (let congress = START_CONGRESS; congress <= END_CONGRESS; congress++) {
        try {
            const responses = await fetchFromWeb(congress);
            const dataByCongress = process(responses);
            data.push(...dataByCongress);
        } catch (err) {
            console.error(err);
        }
    }
    try {
        await insertToDB(data);
    } catch (err) {
        console.error(err);
    }
}


if (require.main === module) {
    main();
}
