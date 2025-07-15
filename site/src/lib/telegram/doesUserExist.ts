import { supabase } from "@/lib/supabase/server";


export default async function doesUserExist(telegramID: number): Promise<boolean>
{
    const tableName = "users_telegram";
    const { count, error } = await supabase
        .from(tableName)
        .select("telegram_id", { head: true, count: "exact" })
        .eq("telegram_id", telegramID)
    if (error) {
        throw new Error(`Error: ${error.message}`);
    }
    return (count ?? 0) > 0;
}
