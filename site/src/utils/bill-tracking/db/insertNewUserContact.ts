import { supabase } from "@/lib/supabase/server";
import { ContactMethod } from "@/types";


export default async function insertNewUserContact(
    userID: string,
    contactMethod: ContactMethod
): Promise<string>
{
    const tableName = "user_contacts";
    const { data, error } = await supabase
        .from(tableName)
        .insert({
            user_id: userID,
            contact_method: contactMethod
        })
        .select("user_contact_id")
        .maybeSingle();
    if (error) {
        throw error;
    }
    if (!data || !data.user_contact_id) {
        throw new Error(`Failed to insert new user contact id`);
    }
    return data.user_contact_id;
}
