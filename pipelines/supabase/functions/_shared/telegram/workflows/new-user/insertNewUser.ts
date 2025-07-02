import { supabase } from "../../../supabase.ts";
import { TelegramMessageChat } from "../../../types.ts";


const TABLE_NAME = "users_telegram";


async function fetchUser(
    linkToken: string
): Promise<{ userID: string, userContactID: string }>
{
    const { data, error } = await supabase
        .from(TABLE_NAME)
        .select('*')
        .eq("link_token", linkToken)
        .single();
    if (error) {
        throw new Error(`Error fetching from table ${TABLE_NAME} via link_token=${linkToken}. Error message: ${error.message}`);
    }
    if (!data.user_id) {
        throw new Error(`Failed to fetch user_id from table ${TABLE_NAME} via link_token=${linkToken}.`)
    }
    if (!data.user_contact_id) {
        throw new Error(`Failed to fetch user_contact_id from table ${TABLE_NAME} via link_token=${linkToken}.`)
    }
    return { userID: data.user_id, userContactID: data.user_contact_id };
}


export default async function insertNewUser(
    linkToken: string,
    chat: TelegramMessageChat
): Promise<void>
{
    const { userID, userContactID} = await fetchUser(linkToken);
    const { error } = await supabase
        .from(TABLE_NAME)
        .update({
            chat_id: chat.id,
            first_name: chat.first_name,
            last_name: chat.last_name,
            username: chat.username
        })
        .eq("link_token", linkToken)
        .eq("user_id", userID)
        .eq("user_contact_id", userContactID);
    if (error) {
        throw new Error(`Error inserting new user to table ${TABLE_NAME} via link_token=${linkToken}, user_id=${userID}, user_contact_id=${userContactID}. Error message: ${error.message}`);
    }
}
