import createLinkToken from "@/lib/create-user/telegram/createLinkToken";
import createUser from "@/lib/create-user/createUser";
import createUserContact from "@/lib/create-user/createUserContact";
import { supabase } from "@/lib/supabase/server";


export default async function createUserTelegram(): Promise<{
    userID: string,
    userContactID: string,
    linkToken: string
}>
{
    const userID = await createUser(supabase);
    const userContactID = await createUserContact(supabase, userID);
    const linkToken = await createLinkToken(supabase, userID, userContactID);
    return { userID, userContactID, linkToken };
}
