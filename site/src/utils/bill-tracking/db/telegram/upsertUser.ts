import { supabase } from "@/lib/supabase/server";
import { TelegramMessageChat } from "@/types";


export default async function upsertUser(
    userID: string,
    userContactID: string,
    chat: TelegramMessageChat
): Promise<void>
{
    const tableName = "users_telegram";
    const { error } = await supabase
        .from(tableName)
        .upsert(
            {
                telegram_id: chat.id,
                user_id: userID,
                user_contact_id: userContactID,
                username: chat.username,
                first_name: chat.first_name,
                last_name: chat.last_name
            },
            { onConflict: "telegram_id" }
        );
    if (error) {
        throw new Error(`Failed to upsert to table ${tableName} for telegram_id=${chat.id}: ${error.message}`);
    }
}
