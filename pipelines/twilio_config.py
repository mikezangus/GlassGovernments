import os
from dotenv import load_dotenv


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(CURRENT_DIR, ".env.local")


load_dotenv(dotenv_path=ENV_PATH)
twilio_sid = os.getenv("TWILIO_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
if not twilio_sid:
    raise RuntimeError(f"Missing Twilio SID")
if not twilio_auth_token:
    raise RuntimeError(f"Missing Twilio auth token")
if not twilio_phone_number:
    raise RuntimeError(f"Missing Twilio phone number")
