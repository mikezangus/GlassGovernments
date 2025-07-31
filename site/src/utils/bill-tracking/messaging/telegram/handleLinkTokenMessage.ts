import { ContactMethod, TelegramMessageChat } from "@/types";
import doesUserExist from "@/utils/bill-tracking/db/telegram/doesUserExist";
import insertNewUser from "@/utils/bill-tracking/db/insertNewUser";
import insertNewUserContact from "@/utils/bill-tracking/db/insertNewUserContact";
import insertSubscriptions from "@/utils/bill-tracking/db/insertSubscriptions";
import fetchHandshake from "@/utils/bill-tracking/db/telegram/fetchHandshake";
import fetchUser from "@/utils/bill-tracking/db/telegram/fetchUser";
import upsertUser from "@/utils/bill-tracking/db/telegram/upsertUser";
import verifyHandshake from "@/utils/bill-tracking/db/telegram/verifyHandshake";


export default async function handleLinkTokenMessage(
    chat: TelegramMessageChat,
    linkToken: string,
): Promise<void>
{
    const telegramID = chat.id;
    let userID: string;
    let userContactID: string;
    if (!(await doesUserExist(telegramID))) {
        userID = await insertNewUser();
        userContactID = await insertNewUserContact(userID, ContactMethod.Telegram);
    } else {
        ({ userID, userContactID } = await fetchUser(telegramID));
    }
    await upsertUser(userID, userContactID, chat);
    const tokenItems = await fetchHandshake(linkToken);
    await insertSubscriptions(userID, tokenItems);
    await verifyHandshake(linkToken);
}
