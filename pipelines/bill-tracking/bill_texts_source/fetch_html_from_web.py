import requests
import time


def fetch_html_from_web(url: str) -> str:
    max_attempts = 5
    retry_delay = 1
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"⚠️ [{attempt}/{max_attempts}] Error on {url}:\n{e}")
            if attempt < max_attempts:
                retry_delay *= attempt
                time.sleep(retry_delay)
            else:
                raise
