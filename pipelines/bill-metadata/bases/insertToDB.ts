import { BillMetadata } from "../types";
import createTable from "../../utils/createTable";
import pool from "../../../localDB";
import { schema, tableName } from "../sql";


export default async function insertToDB(data: BillMetadata[]): Promise<void>
{
    await createTable(tableName, schema);
    const query = `
        INSERT INTO ${tableName}
        (id, congress, type, num, h_vote, h_year, s_vote, s_session, title)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        ON CONFLICT (id) DO NOTHING
    `;
    console.log(`Inserting ${data.length} rows to ${tableName}`);
    let affected = 0;
    for (const item of data) {
        try {
            const result = await pool.query(query, [
                item.id,
                item.congress,
                item.type,
                item.num,
                item.h_vote,
                item.h_year,
                item.s_vote,
                item.s_session,
                item.title
            ]);
            affected += result.rowCount ?? 0;
        } catch (err) {
            console.error(`
                Error: ${err}
                id=${item.id}
                congress=${item.congress}
                type=${item.type}
                num=${item.num}
                h_vote=${item.h_vote}
                h_year=${item.h_year}
                s_vote=${item.s_vote}
                s_session=${item.s_session}
                title=${item.title}
            `);
        }
    }
    console.log(`Inserted ${affected} rows to ${tableName}`);
}
