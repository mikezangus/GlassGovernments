from dotenv import load_dotenv
import os
from supabase import create_client, Client


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
METADATA_DIR = os.path.dirname(CURRENT_DIR)
BILL_TRACKING_DIR = os.path.dirname(METADATA_DIR)
ENV_PATH = os.path.join(BILL_TRACKING_DIR, ".env.local")


load_dotenv(dotenv_path=ENV_PATH)


SUPABASE_API_URL = os.getenv("SUPABASE_API_URL")
if not SUPABASE_API_URL:
    raise RuntimeError("Missing Supabase API URL")

SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
if not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError("Missing Supabase service role Key")


supabase: Client = create_client(SUPABASE_API_URL, SUPABASE_SERVICE_ROLE_KEY)
