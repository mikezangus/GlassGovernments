import { BillText } from "./types";
import createTable from "../utils/createTable";
import pool from "../../db";
import { schema, tableName } from "./sql";


export default async function insertToDB(data: BillText[]): Promise<void>
{
    await createTable(tableName, schema);
    const query = `
        INSERT INTO ${tableName}
        (id, text)
        VALUES ($1, $2)
        ON CONFLICT (id) DO NOTHING
    `;
    console.log(`Inserting ${data.length} rows to ${tableName}`);
    let affected = 0;
    for (const item of data) {
        try {
            const result = await pool.query(query, [item.id, item.text]);
            affected += result.rowCount ?? 0;
        } catch (err) {
            console.error(`
                Error: ${err}
                id=${item.id}
                text=${item.text}
            `);
        }
    }
    console.log(`Inserted ${affected} rows to ${tableName}`);
}
