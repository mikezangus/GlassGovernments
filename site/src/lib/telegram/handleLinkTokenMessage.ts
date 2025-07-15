import { ContactMethod, TelegramMessageChat } from "@/lib/types";
import doesUserExist from "./doesUserExist";
import insertNewUser from "../insertNewUser";
import insertNewUserContact from "../insertNewUserContact";
import fetchUser from "./fetchUser";
import upsertUser from "./upsertUser";
import fetchHandshake from "./fetchHandshake";
import insertSubscriptions from "../insertSubscriptions";
import verifyHandshake from "./verify_handshake";


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
