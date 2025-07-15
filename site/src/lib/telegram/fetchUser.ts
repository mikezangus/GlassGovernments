import { supabase } from "@/lib/supabase/server";


export default async function fetchUser(
    telegramID: number
): Promise<{ userID: string, userContactID: string}>
{
    const tableName = "users_telegram";
    const { data, error } = await supabase
        .from(tableName)
        .select("user_id, user_contact_id")
        .eq("telegram_id", telegramID)
        .single();
    if (error) {
        throw new Error(`Error fetching from table ${tableName} via telegram_id=${telegramID}. Error: ${error.message}`);
    }
    if (!data.user_id) {
        throw new Error(`No user_id from table ${tableName} via telegram_id=${telegramID}`);
    }
    if (!data.user_contact_id) {
        throw new Error(`No user_contact_id from table ${tableName} via telegram_id=${telegramID}`);
    }
    return { userID: data.user_id, userContactID: data.user_contact_id };
}
