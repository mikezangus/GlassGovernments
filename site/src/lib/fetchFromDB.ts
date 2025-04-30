import { db } from "./db";


export default async function fetchFromDB<T = any>
(
    table: string,
    {
        select = '*',
        filters = [],
        limit,
        single = false
    }: {
        select?: string;
        filters?: { column: string; operator: string; value: any }[];
        limit?: number;
        single?: boolean;
    } = {}
): Promise<T[] | T | null>
{
    let query = db.from(table).select(select);
    for (const { column, operator, value } of filters) {
        query = query.filter(column, operator as any, value);
    }
    if (limit !== undefined) {
        query = query.limit(limit);
    }
    const { data, error } = single
        ? await query.single()
        : await query;
    if (error) {
        throw error;
    }
    return data as T | T[];
}
