import { supabase } from "@/lib/supabase/server";
import { TokenItemRow } from "@/lib/types";


export default async function insertSubscriptions(
    userID: string,
    tokenItems: TokenItemRow[],
): Promise<void>
{
    const tableName = "subscriptions";
    if (tokenItems.length === 0) {
        return
    };
    const rows: { user_id: string, token: string, state: string }[] = [];
    for (const { token, state } of tokenItems) {
        rows.push({ user_id: userID, token, state});
    }
    const { error } = await supabase
        .from(tableName)
        .upsert(rows, { ignoreDuplicates: true });
    if (error)
        throw new Error(`insertSubscriptions: ${error.message} (user_id=${userID})`);
}
