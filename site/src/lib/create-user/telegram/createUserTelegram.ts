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
    console.log(`createUserTelegram | userID=${userID}`);
    const userContactID = await createUserContact(supabase, userID);
    console.log(`createUserTelegram | userContactID=${userContactID}`);
    const linkToken = await createLinkToken(supabase, userID, userContactID);
    console.log(`createUserTelegram | linkToken=${linkToken}`);
    return { userID, userContactID, linkToken };
}
