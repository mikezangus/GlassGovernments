import { BillMetadata } from "../types";
import pool from "../../../db";
import { tableName } from "../sql";


export default async function insertToDB(data: BillMetadata[]): Promise<void>
{
    const query = `
        UPDATE ${tableName}
        SET
            h_vote = $2,
            h_year = $3,
            s_vote = $4,
            s_session = $5
        WHERE id = $1 AND (
            h_vote IS DISTINCT FROM $2 OR
            h_year IS DISTINCT FROM $3 OR
            s_vote IS DISTINCT FROM $4 OR
            s_session IS DISTINCT FROM $5
        );
    `;
    console.log(`Inserting ${data.length} rows to ${tableName}`);
    let affected = 0;
    for (const item of data) {
        try {
            const result = await pool.query(query, [
                item.id,
                item.h_vote,
                item.h_year,
                item.s_vote,
                item.s_session
            ]);
            affected += result.rowCount ?? 0;
        } catch (err) {
            console.error(err);
            throw err;
        }  
    }
    console.log(`Inserted ${affected} rows to ${tableName}`);
}
