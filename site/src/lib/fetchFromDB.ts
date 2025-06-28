import { supabase } from "@/lib/supabase";


type FilterValue = string | number | boolean | null;


interface Filter {
    column: string;
    operator: string;
    value: FilterValue | FilterValue[];
}


interface FetchOptions {
    select?: string;
    filters?: Filter[];
    limit?: number;
    single?: boolean;
}


export default async function fetchFromDB<T>
(
    table: string,
    {
        select = '*',
        filters = [],
        limit,
        single = false
    }: FetchOptions = {}
): Promise<T[] | T | null>
{
    let query = supabase
        .from(table)
        .select(select);
    for (const { column, operator, value } of filters) {
        query = query.filter(column, operator, value);
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
