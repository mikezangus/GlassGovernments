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
    if (error) {
        throw new Error(`Failed to insert new row to table users. Error: ${error.message}`);
    }
    if (!data.user_id) {
        throw new Error(`Failed to select user_id from new row inserted to table users.`);
    }
    return data.user_id;
}
