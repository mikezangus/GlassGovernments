import os
from dotenv import load_dotenv


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(CURRENT_DIR, ".env.local")


load_dotenv(dotenv_path=ENV_PATH)
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
if not supabase_url or not supabase_key:
    raise RuntimeError("Missing env vars")


supabase_headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}
