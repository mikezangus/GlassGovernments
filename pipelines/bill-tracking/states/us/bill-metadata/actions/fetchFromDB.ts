import { BillMetadata } from "../types";
import pool from "../../../../localDB";
import { tableName } from "../sql";


export default async function fetchFromDB(congress: number): Promise<BillMetadata[]>
{
    const query = `
        SELECT * FROM ${tableName}
        WHERE congress = $1
        AND (h_vote = 0 OR s_vote = 0)`;
    try {
        const result = await pool.query(query, [congress]);
        return result.rows;
    } catch (err) {
        console.error(err);
        throw err;
    }
}
