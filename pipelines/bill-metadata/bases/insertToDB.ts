import { PoolConnection } from "mysql2/promise";
import { Bill } from "../types";
import pool from "../../../db";
import { schema, tableName } from "../schema";


async function createTable(connection: PoolConnection): Promise<void>
{
    const query = `CREATE TABLE IF NOT EXISTS ${tableName} (${schema});`;
    try {
        await connection.execute(query);
    } catch (err) {
        console.error(err);
        throw err;
    }
}


export default async function insertToDB(data: Bill[]): Promise<void>
{
    const connection = await pool.getConnection();
    await createTable(connection);
    const query = `
        INSERT IGNORE INTO ${tableName}
        (id, congress, type, num, action)
        VALUES (?, ?, ?, ?, ?)
    `;
    console.log(`\nStarted inserting ${data.length} rows to ${tableName}`);
    try {
        for (const item of data) {
            try {
                connection.execute(
                    query,
                    [item.id, item.congress, item.type, item.num, item.action]
                );
            } catch (err) {
                console.error(`id=${item.id} | congress=${item.congress} | type=${item.type} | num = ${item.num} | action=${item.action}`);
                console.error(err);
                throw err;
            }
        }
    } catch (err) {
        console.error(err);
    } finally {
        if (connection) {
            connection.release();
        }
        await pool.end();
    }
}
