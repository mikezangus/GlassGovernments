import os
import requests
import sys
from pathlib import Path
from typing import Tuple

processing_dir = Path(__file__).resolve().parent
data_dir = str(processing_dir.parent)
sys.path.append(data_dir)
from directories import get_locations_file_path


def generate_all_zip_codes() -> list:
    zip_codes = [f"{i:05d}" for i in range (500, 100000)]
    return zip_codes


def verify_coordinates_in_usa(lat: float, lon: float) -> bool:
    n = 72
    s = 18
    e = -67
    w = -179.999999
    return s <= lat <= n and w <= lon <= e


def get_coordinates(session: requests.Session, zip_code: str) -> Tuple[float | None, float | None]:
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": zip_code,
        "format": "json"
    }
    try:
        response = session.get(
            url,
            params = params,
            timeout = 10
        )
        response.raise_for_status()
        data = response.json()
        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return lat, lon
    except Exception as e:
        print(f"{zip_code} | Error:", e)
    return None, None


def append_file(zip_code: str, lat: float, lon: float) -> None:
    if verify_coordinates_in_usa(lat, lon):
        path = get_locations_file_path()
        with open(path, "a") as f:
            header = "ZIP,LAT,LON\n" if os.stat(path).st_size == 0 else ""
            line = f"{zip_code},{lat},{lon}\n"
            f.write(header + line)
    else:
        print(f"{zip_code} | Not in USA ({lat}, {lon})")
    return


def get_locations(zip_codes: list) -> None:
    session = requests.Session()
    zip_code_count = f"{len(zip_codes):,}"
    for zip_code in zip_codes:
        lat, lon = get_coordinates(session, zip_code)
        if lat and lon:
            append_file(zip_code, lat, lon)
    print(f"Finished writing {zip_code_count} locations")
    return


def main():
    zip_codes = generate_all_zip_codes()
    get_locations(zip_codes)


if __name__ == "__main__":
    main()
