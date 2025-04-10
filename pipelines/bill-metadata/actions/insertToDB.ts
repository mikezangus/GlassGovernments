import pool from "../../../db";
import { tableName } from "../sql";
import { Bill } from "../types";


export default async function insertToDB(data: Bill[], congress: number): Promise<void>
{
    const query = `
        UPDATE ${tableName}
        SET action = TRUE
        WHERE id = $1;
    `;
    try {
        let affected = 0;
        data = data.filter(item => item.action === true);
        for (const item of data) {
            const result = await pool.query(query, [item.id]);
            affected += result.rowCount ?? 0;
        }
        console.log(`Updated ${affected} ${tableName} rows for Congress ${congress}`);
    } catch (err) {
        console.error(err);
        throw err;
    }  
}
