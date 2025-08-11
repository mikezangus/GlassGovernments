import pool from "../../../localDB";


export default async function insertToDB(
    data: any[],
    tableName: string,
    query: string,
    paramMapper: (row: any) => []
): Promise<void>
{
    console.log(`Inserting to ${tableName}`);
    let affected = 0;
    for (const row of data) {
        try {
            const result = await pool.query(query, paramMapper(row));
            affected += result.rowCount ?? 0;
        } catch (err) {
            console.error(`⚠️ Error: ${err}\nRow: ${row}\n`);
        }
    }
    console.log(`Inserted ${affected} rows to ${tableName}`);
}
