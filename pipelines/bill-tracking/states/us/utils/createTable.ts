import pool from "../../../localDB";


export default async function createTable(
    tableName: string, schema: string
): Promise<void>
{
    const query = `CREATE TABLE IF NOT EXISTS ${tableName} (${schema});`;
    try {
        await pool.query(query);
    } catch (err) {
        console.error(err);
        throw err;
    }
}
