import { SupabaseClient } from "@supabase/supabase-js";


export default async function createLinkToken(
    supabase: SupabaseClient,
    userID: string,
    userContactID: string
): Promise<string>
{
    const { data, error } = await supabase
        .from("users_telegram")
        .insert({
            user_id: userID,
            user_contact_id: userContactID
        })
        .select("link_token")
        .single();
    if (error || !data.link_token) {
        throw new Error(`Failed to create Telegram link token. Error: ${error?.message}\nData: ${data}`);
    }
    return data.link_token;
}
