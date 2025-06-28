import createUser from "@/lib/createUser";
import createUserContact from "@/lib/createUserContact";
import createUserTelegramToken from "@/lib/createUserTelegramToken";
import { ContactType } from "@/lib/types";
import { supabase } from "@/lib/supabase";



export default async function createUserTelegram(
    contactValue: string
): Promise<{ userID: string, userContactID: string, telegramToken: string }>
{
    const userID = await createUser(supabase);
    const userContactID = await createUserContact(
        supabase,
        userID,
        ContactType.Telegram,
        contactValue
    );
    const telegramToken = await createUserTelegramToken(supabase, userID);
    return { userID, userContactID, telegramToken };
}
