import { supabase } from "@/lib/supabase/server";
import { WordAndState } from "@/lib/types";


export default async function fetchHandshake(
    linkToken: string,
): Promise<WordAndState[]>
{
    const tableName = "telegram_handshakes";
    const { data, error } = await supabase
        .from(tableName)
        .select("word, state")
        .eq("link_token", linkToken)
    if (error) {
        throw new Error(`Error on table ${tableName}: ${error.message}`);
    }
    if (!data || data.length === 0) {
        throw new Error(`No rows on table ${tableName} for ${linkToken}`);
    }
    return data as WordAndState[];
}
