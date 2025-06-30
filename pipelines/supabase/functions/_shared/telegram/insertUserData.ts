import { createClient, SupabaseClient } from "@supabase/supabase-js";


const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;


async function fetchIDs(
    supabase: SupabaseClient,
    linkToken: string
): Promise<{ userID: string, userContactID: string }>
{
    const { data, error } = await supabase
        .from("users_telegram")
        .select('*')
        .eq("link_token", linkToken)
        .single();
    if (error || !data.user_id || !data.user_contact_id) {
        throw new Error(`Error fetching IDs: ${error}`);
    }
    return { userID: data.user_id, userContactID: data.user_contact_id };
}


export default async function insertUserData(
    message: any,
    linkToken: string,

): Promise<void>
{
    const chat = message.chat;
    const channelID = chat.id;
    const firstName = chat.first_name ?? null;
    const lastName = chat.last_name ?? null;
    const username = chat.username ?? null;
    const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);
    const { userID, userContactID } = await fetchIDs(supabase, linkToken);
    const { error } = await supabase
        .from("users_telegram")
        .update({
            telegram_id: channelID,
            first_name: firstName,
            last_name: lastName,
            username: username,
            used: true,
        })
        .eq("user_id", userID)
        .eq("user_contact_id", userContactID);
    if (error) {
        throw new Error(`Error inserting user data: ${error}`);
    }
}
