import { ContactType } from "@/lib/types";
import { SupabaseClient } from "@supabase/supabase-js";


export default async function createUserContact(
    supabase: SupabaseClient,
    userID: string,
    contactType: ContactType,
    contactValue: string
): Promise<string>
{
    const { data, error } = await supabase
        .from("user_contacts")
        .insert({
            user_id: userID,
            contact_type: contactType,
            contact_value: contactValue
        })
        .select("id")
        .single();
    if (error || !data.id) {
        throw error;
    }
    return data.id;
}
