import { supabase } from "./supabase";


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
        ? supabase.from(tableName).upsert(rows, { onConflict: conflictColumns })
        : supabase.from(tableName).insert(rows);
    const { error } = await query;
    if (error) {
        throw new Error(`Error inserting to ${tableName}: ${error.message}`);
    }
}
