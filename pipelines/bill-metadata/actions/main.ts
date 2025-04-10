import pLimit from "p-limit";
import { spawn } from "child_process";
import pool from "../../../db";
import deleteUnactionedRows from "./deleteUnactionedRows";
import fetchFromDB from "./fetchFromDB";
import fetchFromWeb from "./fetchFromWeb";
import insertToDB from "./insertToDB";





async function driver(congress: number)
{
    try {
        let data = await fetchFromDB(congress);
        await fetchFromWeb(data);
        data = data.filter(item => item.action === false);
        await insertToDB(data);
        if (congress !== 119) {
            await deleteUnactionedRows(congress);
        }
    } catch (err) {
        console.error(err);
    } finally {
        await pool.end();
    }
}


async function main(startArg: string | undefined, endArg: string | undefined)
{
    console.log("yay", startArg);
    console.log("yay", endArg);
    if (startArg && endArg) {
        const startCongress = parseInt(startArg);
        const endCongress = parseInt(endArg);
        if (isNaN(startCongress) || isNaN(endCongress)) {
            process.exit(1);
        }
        const limit = pLimit(8);
        const tasks = [];
        for (let congress = startCongress; congress <= endCongress; congress++) {
            const task = limit(() =>
                new Promise<void>((resolve, reject) => {
                    const child = spawn("npx", ["ts-node", __filename, congress.toString()], {
                        stdio: "inherit",
                        env: process.env,
                    });
                    child.on("exit", (code) => {
                        console.log(`\n\nCongress ${congress} finished with exit code ${code}\n\n`);
                        resolve();
                    });
                    child.on("error", (err) => {
                        console.error(`Error running Congress ${congress}`, err);
                        reject(err);
                    });
                })
            );
            tasks.push(task);
        }
        await Promise.all(tasks);
    } else if (startArg) {
        const congress = parseInt(startArg);
        if (isNaN(congress)) {
            console.error(`Failed to parse congress=${startArg} to int`);
            process.exit(1);
        }
        await driver(congress);
    } else {
        console.error("Failed to run. Use:\nnpx ts-node main.ts {startCongress} {endCongress}");
        process.exit(1);
    }
}


if (require.main === module) {

    main(process.argv[2], process.argv[3]);

}
