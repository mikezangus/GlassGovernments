import { TelegramMessageChat, TokenItem } from "../types";
import { supabase } from "../supabase/server";


async function doesTelegramUserExist(telegramID: number): Promise<boolean>
{
    const tableName = "users_telegram";
    const { count, error } = await supabase
        .from(tableName)
        .select("telegram_id", { head: true, count: "exact" })
        .eq("telegram_id", telegramID)
    if (error) {
        throw new Error(``)
    }
    return (count ?? 0) > 0;
}


async function insertNewUser(): Promise<string>
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


async function insertNewUserContact(
    userID: string
): Promise<string>
{
    const tableName = "user_contacts";
    const { data, error } = await supabase
        .from(tableName)
        .insert({
            user_id: userID,
            contact_method: "telegram"
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


async function fetchExistingTelegramUser(
    telegramID: number
): Promise<{ userID: string, userContactID: string}>
{
    const tableName = "users_telegram";
    const { data, error } = await supabase
        .from(tableName)
        .select("user_id, user_contact_id")
        .eq("telegram_id", telegramID)
        .single();
    if (error) {
        throw new Error(`Error fetching from table users_telegram via telegram_id=${telegramID}. Error: ${error.message}`);
    }
    if (!data.user_id) {
        throw new Error(`Failed to fetch user_id from table users_telegram via telegram_id=${telegramID}. No data returned`);
    }
    if (!data.user_contact_id) {
        throw new Error(`Failed to fetch user_contact_id from table users_telegram via telegram_id=${telegramID}. No data returned`);
    }
    return { userID: data.user_id, userContactID: data.user_contact_id };
}


async function upsertTelegramUser(
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


async function fetchTokenItems(
    linkToken: string
): Promise<TokenItem[]>
{
    const tableName = "telegram_handshakes";
    const { data, error } = await supabase
        .from(tableName)
        .select("token_items")
        .eq("link_token", linkToken)
        .maybeSingle();
    if (error)
    throw new Error(
      `fetchTokenItems: ${error.message} (link_token=${linkToken})`
    );
    if (!data?.token_items)
        throw new Error(`fetchTokenItems: no token_items for ${linkToken}`);
    return data.token_items as TokenItem[];
}


async function insertSubscriptions(
    userID: string,
    tokenItems: TokenItem[]
): Promise<void>
{
    const tableName = "subscriptions";
    if (tokenItems.length === 0) {
        return
    };
    const rows = tokenItems.flatMap(({ token, states }) =>
        states.map((state) => ({
            user_id: userID,
            token,
            state,
        }))
    );
    const { error } = await supabase
        .from(tableName)
        .upsert(
            rows,
            { onConflict: "user_id,token,state" }
        );

    if (error)
        throw new Error(`insertSubscriptions: ${error.message} (user_id=${userID})`);
}


export default async function handleLinkTokenMessage(
    chat: TelegramMessageChat,
    linkToken: string,
): Promise<void>
{
    const telegramID = chat.id;
    let userID: string;
    let userContactID: string;
    if (!(await doesTelegramUserExist(telegramID))) {
        userID = await insertNewUser();
        userContactID = await insertNewUserContact(userID);
    } else {
        ({ userID, userContactID } = await fetchExistingTelegramUser(telegramID));
    }
    await upsertTelegramUser(userID, userContactID, chat);
    const tokenItems = await fetchTokenItems(linkToken);
    await insertSubscriptions(userID, tokenItems);
}
