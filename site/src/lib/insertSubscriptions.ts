import { supabase } from "@/lib/supabase/server";
import { WordAndState } from "@/lib/types";


export default async function insertSubscriptions(
    userID: string,
    items: WordAndState[],
): Promise<void>
{
    const tableName = "subscriptions";
    if (items.length === 0) {
        return
    };
    const rows: { user_id: string, word: string, state: string }[] = [];
    for (const { word, state } of items) {
        rows.push({ user_id: userID, word, state});
    }
    const { error } = await supabase
        .from(tableName)
        .upsert(rows, { ignoreDuplicates: true });
    if (error)
        throw new Error(`insertSubscriptions: ${error.message} (user_id=${userID})`);
}
