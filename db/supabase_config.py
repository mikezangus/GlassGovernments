from dotenv import load_dotenv
from supabase import create_client, Client
import os


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINES_DIR = os.path.dirname(CURRENT_DIR)
ENV_PATH = os.path.join(PIPELINES_DIR, ".env.local")


load_dotenv(dotenv_path=ENV_PATH)


def _print_error(str: str) -> str:
    return f"Failed to load {str} from environment file"


SUPABASE_URL_API = os.getenv("SUPABASE_URL_API")
if not SUPABASE_URL_API:
    raise RuntimeError(_print_error("SUPABASE_URL_API"))


SUPABASE_URL_DIRECT = os.getenv("SUPABASE_URL_DIRECT")
if not SUPABASE_URL_DIRECT:
    raise RuntimeError(_print_error("SUPABASE_URL_DIRECT"))


SUPABASE_URL_POOL = os.getenv("SUPABASE_URL_POOL")
if not SUPABASE_URL_POOL:
    raise RuntimeError(_print_error("SUPABASE_URL_POOL"))


SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
if not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError(_print_error)


supabase: Client = create_client(SUPABASE_URL_API, SUPABASE_SERVICE_ROLE_KEY)
