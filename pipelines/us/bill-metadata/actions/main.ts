import currentCongress from "../../../utils/currentCongress";
import fetchFromDB from "./fetchFromDB";
import fetchFromWeb from "./fetchFromWeb";
import insertToDB from "./insertToDB";
import pool from "../../../../localDB";


async function main(startArg: string | undefined, endArg: string | undefined)
{
    if (!startArg) {
        process.exit(1);
    } else if (!endArg) {
        endArg = startArg;
    }
    const startCongress = parseInt(startArg);
    const endCongress = parseInt(endArg);
    if (isNaN(startCongress) || isNaN(endCongress)) {
        process.exit(1);
    }
    for (
        let congress = startCongress;
        congress <= endCongress && congress >= 102 && congress <= currentCongress();
        congress++
    ) {
        try {
            const data = await fetchFromDB(congress);
            await fetchFromWeb(data);
            await insertToDB(data);
        } catch (err) {
            console.error(err);
        }
    }
    await pool.end();
}


if (require.main === module) {
    main(process.argv[2], process.argv[3]);
}
