import { Bill } from "../types";
import pool from "../../../db";
import { schema, tableName } from "../sql";


async function createTable(): Promise<void>
{
    const query = `CREATE TABLE IF NOT EXISTS ${tableName} (${schema});`;
    try {
        await pool.query(query);
    } catch (err) {
        console.error(err);
        throw err;
    }
}


export default async function insertToDB(data: Bill[]): Promise<void>
{
    await createTable();
    const query = `
        INSERT INTO ${tableName} (id, congress, type, num, action)
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (id) DO NOTHING
    `;
    console.log(`\nStarted inserting ${data.length} rows to ${tableName}`);
    for (const item of data) {
        try {
            await pool.query(
                query,
                [item.id, item.congress, item.type, item.num, item.action]
            );
        } catch (err) {
            console.error(`Error:\nid=${item.id} | congress=${item.congress} | type=${item.type} | num = ${item.num} | action=${item.action}`);
        }
    }
}
