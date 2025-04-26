import requests
import time


def fetch_html_from_web(url: str) -> str:
    max_attempts = 5
    retry_delay = 1
    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"⚠️ [{attempt}/{max_attempts}] Error on {url}:\n{e}")
            if attempt < max_attempts:
                retry_delay *= attempt
                time.sleep(retry_delay)
            else:
                raise
