import { supabase } from "@/lib/supabase/server";


export default async function insertNewUser(): Promise<string>
{
    const tableName = "users";
    const { data, error } = await supabase
        .from(tableName)
        .insert({})
        .select("user_id")
        .maybeSingle();
    if (error) {
        throw error;
    }
    if (!data || !data.user_id) {
        throw new Error(`Failed to insert new user`);
    }
    return data.user_id;
}
