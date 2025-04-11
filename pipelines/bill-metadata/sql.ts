import pool from "../../db";


export const tableName = "bill_metadata";


export const schema = `
    id VARCHAR(15) PRIMARY KEY,
    congress SMALLINT,
    type VARCHAR(7),
    num VARCHAR(5),
    title TEXT,
    action BOOLEAN DEFAULT FALSE
`;


export async function createTable(): Promise<void>
{
    const query = `CREATE TABLE IF NOT EXISTS ${tableName} (${schema});`;
    try {
        await pool.query(query);
    } catch (err) {
        console.error(err);
        throw err;
    }
}
