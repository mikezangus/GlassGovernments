import { SupabaseClient } from "@supabase/supabase-js";


export default async function createUserTelegramToken(
    supabase: SupabaseClient,
    userID: string,
): Promise<string>
{
    const { data, error } = await supabase
        .from("user_telegram_tokens")
        .insert({ user_id: userID })
        .select("telegram_token")
        .single();
    if (error || !data.telegram_token) {
        throw error;
    }
    return data.telegram_token;
}
