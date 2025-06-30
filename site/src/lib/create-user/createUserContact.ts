import { SupabaseClient } from "@supabase/supabase-js";


export default async function createUserContact(
    supabase: SupabaseClient,
    userID: string
): Promise<string>
{
    const { data, error } = await supabase
        .from("user_contacts")
        .insert({ user_id: userID })
        .select("user_contact_id")
        .single();
    if (error || !data.user_contact_id) {
        throw new Error("Failed to create user contact");
    }
    return data.user_contact_id;
}
