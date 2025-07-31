import { supabase } from "@/lib/supabase/server";


export default async function fetchTelegramID(userID: string): Promise<number | null>
{
    const { data, error } = await supabase
        .from("users_telegram")
        .select("telegram_id")
        .eq("user_id", userID)
        .maybeSingle();
    if (error) {
        throw new Error(`fetchTelegramChatId: ${error.message}`);
    }
    return data?.telegram_id ?? null;
}
