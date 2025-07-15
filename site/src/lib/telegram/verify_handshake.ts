import { supabase } from "../supabase/server";


export default async function verifyHandshake(
    linkToken: string,
): Promise<void>
{
    const tableName = "telegram_handshakes";
    const { error } = await supabase
        .from(tableName)
        .update({ verified: true })
        .eq("link_token", linkToken);
    if (error) {
        throw error;
    }
}
