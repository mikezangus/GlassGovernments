import { createClient } from "@supabase/supabase-js";


const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;


export const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);
