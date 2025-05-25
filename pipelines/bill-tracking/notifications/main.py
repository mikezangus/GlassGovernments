import psycopg2
from datetime import datetime
from twilio.rest import Client
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINES_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PIPELINES_DIR)
from supabase_config import supabase_db_url
from twilio_config import twilio_sid, twilio_auth_token, twilio_phone_number


client = Client(twilio_sid, twilio_auth_token)


def send_sms(to_number: str, message: str):
    message = client.messages.create(
        to=f"+1{to_number}",
        from_=twilio_phone_number,
        body=message
    )
    return message.sid


def fetch_state_subscriptions():
    connection = psycopg2.connect(supabase_db_url)
    cursor = connection.cursor()
    cursor.execute("select * from get_stale_subscriptions()")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def update_last_sent(subscription_id: str):
    connection = psycopg2.connect(supabase_db_url)
    cursor = connection.cursor()
    cursor.execute("""
        update subscriptions
        set last_sent = now()
        where id = %s
    """, (subscription_id,))
    connection.commit()
    cursor.close()
    connection.close()


def notify_users():
    subscriptions = fetch_state_subscriptions()
    for subscription in subscriptions:
        subscription_id, user_id, token, state, bill_id, pubdate, phone_number = subscription
        message = f"Update for {token} in {state}:\n{bill_id} updated on {pubdate}"
        try:
            sid = send_sms(phone_number, message)
            print(f"Sent to {phone_number} from {twilio_phone_number}: SID {sid}")
            update_last_sent(subscription_id)
        except Exception as e:
            print(f"Failed to notify {phone_number} from {twilio_phone_number}: {e}")


if __name__ == "__main__":
    notify_users()
