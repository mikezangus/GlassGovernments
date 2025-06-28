import { SupabaseClient } from "@supabase/supabase-js";


export default async function createUser(
    supabase: SupabaseClient
): Promise<string>
{
    const { data, error } = await supabase
        .from("users")
        .insert({})
        .select("user_id")
        .single();
    if (error || !data.user_id) {
        throw error;
    }
    return data.user_id;
}
