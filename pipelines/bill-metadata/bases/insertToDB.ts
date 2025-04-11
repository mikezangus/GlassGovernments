import { Bill } from "../types";
import { createTable, tableName } from "../sql";
import pool from "../../../db";


export default async function insertToDB(data: Bill[]): Promise<void>
{
    await createTable();
    const query = `
        INSERT INTO ${tableName} (id, congress, type, num, title, action)
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (id) DO NOTHING
    `;
    console.log(`Inserting ${data.length} rows to ${tableName}`);
    for (const item of data) {
        try {
            await pool.query(
                query,
                [item.id, item.congress, item.type, item.num, item.title, item.action]
            );
        } catch (err) {
            console.error(`Error:\nid=${item.id} | congress=${item.congress} | type=${item.type} | num=${item.num} | title=${item.title} | action=${item.action}`);
        }
    }
}
