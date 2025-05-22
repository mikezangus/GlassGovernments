import { db } from "./db";


export default async function insertToDB<T extends Record<string, unknown>>(
    tableName: string,
    rows: T[],
    conflictColumns?: string | string[]
): Promise<void>
{
    if (rows.length === 0) {
        return;
    }
    if (conflictColumns && Array.isArray(conflictColumns)) {
        conflictColumns = conflictColumns.join(",");
    }
    const query = conflictColumns
            ? db.from(tableName).upsert(rows, { onConflict: conflictColumns })
            : db.from(tableName).insert(rows);
    const { error } = await query;
    if (error) {
        throw new Error(`Error inserting to ${tableName}: ${error.message}`);
    }
}
