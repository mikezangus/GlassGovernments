from dotenv import load_dotenv
from supabase import create_client, Client
import os


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINES_DIR = os.path.dirname(CURRENT_DIR)
SRC_DIR = os.path.dirname(PIPELINES_DIR)
ENV_PATH = os.path.join(SRC_DIR, ".env.local")


load_dotenv(dotenv_path=ENV_PATH)


def _print_error(str: str) -> str:
    return f"Failed to load {str} from environment file"


supabase_api_url = os.getenv("SUPABASE_URL_API")
if not supabase_api_url:
    raise RuntimeError(_print_error("SUPABASE_URL_API"))


supabase_direct_url = os.getenv("SUPABASE_URL_DIRECT")
if not supabase_direct_url:
    raise RuntimeError(_print_error("SUPABASE_URL_DIRECT"))


supabase_pool_url = os.getenv("SUPABASE_URL_POOL")
if not supabase_pool_url:
    raise RuntimeError(_print_error("SUPABASE_URL_POOL"))


supabase_service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
if not supabase_service_role_key:
    raise RuntimeError(_print_error)


supabase: Client = create_client(supabase_api_url, supabase_service_role_key)
