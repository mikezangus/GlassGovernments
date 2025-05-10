import { db } from "./db";


export default async function insertToDB<T extends Record<string, unknown>>(
    table: string, rows: T[], conflictColumn?: string
): Promise<void>
{
    const query = conflictColumn
            ? db.from(table).upsert(rows, { onConflict: conflictColumn })
            : db.from(table).insert(rows);
    const { error } = await query;
    if (error) {
        throw error
    }
}
