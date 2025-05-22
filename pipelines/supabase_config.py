import os
from dotenv import load_dotenv


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(CURRENT_DIR, ".env.local")


load_dotenv(dotenv_path=ENV_PATH)
supabase_api_url = os.getenv("SUPABASE_API_URL")
supabase_api_key = os.getenv("SUPABASE_API_KEY")
supabase_db_url = os.getenv("SUPABASE_DB_URL")
if not supabase_api_url:
    raise RuntimeError("Missing Supabase API URL")
if not supabase_api_key:
    raise RuntimeError("Missing Supabase API Key")
if not supabase_db_url:
    raise RuntimeError("Missing Supabase DB URL")


supabase_headers = {
    "apikey": supabase_api_key,
    "Authorization": f"Bearer {supabase_api_key}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}
