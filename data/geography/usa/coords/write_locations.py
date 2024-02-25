import json
import logging
import os
import requests
import sys
from create_log import create_log

coords_dir = os.path.dirname(__file__)
usa_dir = os.path.dirname(coords_dir)
geography_dir = os.path.dirname(usa_dir)
data_dir = os.path.dirname(geography_dir)
sys.path.append(data_dir)
from directories import get_config_file_path, get_data_files_dir


def get_api_key() -> str:
    path = get_config_file_path()
    with open(path, "r") as config_file:
        config = json.load(config_file)
    api_key = config["googleMapsAPIKey"]
    print("Google Maps API Key retrieved")
    return api_key


def generate_all_zip_codes() -> list:
    zip_codes = [f"{i:05d}" for i in range (500, 100000)]
    print("ZIP Codes generated")
    return zip_codes


def get_coords_osm(session: requests.Session, zip_code: str) -> tuple[float | None, float | None]:
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "postalcode": zip_code,
        "countrycodes": "us",
        "format": "json",
        "limit": 1
    }
    try:
        response = session.get(
            url,
            params = params,
            timeout = 60
        )
        response.raise_for_status()
        data = response.json()
        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return lat, lon
    except Exception as e:
        msg = f"{zip_code} | Error: {e}"
        print(msg)
        logging.info(msg)
    return None, None


def get_coords_google(session: requests.Session, zip_code: str, api_key: str) -> tuple[float | None, float | None]:
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "components": f"postal_code:{zip_code}|country:US",
        "key": api_key
    }
    try:
        response = session.get(
            url = url,
            params = params,
            timeout = 60
        )
        response.raise_for_status()
        data = response.json()
        if data["results"]:
            location = data["results"][0]["geometry"]["location"]
            lat = location["lat"]
            lon = location["lng"]
            return lat, lon
    except Exception as e:
        msg = f"{zip_code} | Error: {e}"
        print(msg)
        logging.info(msg)
    return None, None


def append_file(zip_code: str, lat: float, lon: float) -> None:
    path = os.path.join(get_data_files_dir(), "locations.csv")
    with open(path, "a") as f:
        header = "ZIP,LAT,LON\n" if os.stat(path).st_size == 0 else ""
        line = f"{zip_code},{lat},{lon}\n"
        f.write(header + line)
    return


def get_locations(zip_codes: list, api_key: str) -> None:
    session = requests.Session()
    zip_code_count = len(zip_codes)
    pct_interval = max(zip_code_count // 10, 1)
    for i, zip_code in enumerate(zip_codes, start = 1):
        lat, lon = get_coords_google(session, zip_code, api_key)
        if lat and lon:
            append_file(zip_code, lat, lon)
        else:
            logging.info(f"No coords for ZIP code: {zip_code}")
        if i % pct_interval == 0 or i == zip_code_count:
            print(f"{(i / zip_code_count) * 100}% complete")
    print(f"Finished writing locations")
    return


def main():
    create_log()
    zip_codes = generate_all_zip_codes()
    api_key = get_api_key()
    get_locations(zip_codes, api_key)


if __name__ == "__main__":
    main()
