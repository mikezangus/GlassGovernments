import { spawn } from "child_process";
import { Bill } from "../types";
import fetchFromWeb from "./fetchFromWeb";
import insertToDB from "./insertToDB";
import process from "./process";
import pool from "../../../db";


const START_CONGRESS = 1;
const END_CONGRESS = 119;


async function main()
{
    const caffeinate = spawn(
        "caffeinate",
        ["-d", "-i", "-s", "-u"],
        { detached: false, stdio: "ignore" }
    );
    for (let congress = START_CONGRESS; congress <= END_CONGRESS; congress++) {
        const data: Bill[] = [];
        try {
            const responses = await fetchFromWeb(congress);
            data.push(...process(responses));
            await insertToDB(data);
        } catch (err) {
            console.error(err);
        }
    }
    await pool.end();
    caffeinate.kill("SIGTERM");
}


if (require.main === module) {
    main();
}
