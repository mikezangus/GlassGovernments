import { Bill } from "../types";
import { createTable, tableName } from "../sql";
import pool from "../../../db";


export default async function insertToDB(data: Bill[]): Promise<void>
{
    await createTable();
    const query = `
        INSERT INTO ${tableName}
        (id, congress, type, num, h_vote, h_year, s_vote, s_session, title)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        ON CONFLICT (id) DO NOTHING
    `;
    console.log(`Inserting ${data.length} rows to ${tableName}`);
    for (const item of data) {
        try {
            await pool.query(query, [
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
}
