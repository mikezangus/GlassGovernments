import pool from "../../../db";
import { tableName } from "../sql";


export default async function deleteUnactionedRows(congress: number): Promise<void>
{
    const query = `DELETE FROM ${tableName} WHERE congress = $1 AND action = FALSE`;
    try {
        const result = await pool.query(query, [congress]);
        console.log(`Deleted ${result.rowCount} unactioned rows for Congress ${congress}`);
    } catch (err) {
        console.error(err);
        throw err;
    }
}
