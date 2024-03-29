import geopandas as gpd
import json
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSING_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PROCESSING_DIR)
from utils.get_mongo_config import get_mongo_config
from utils.upload_df import upload_df

DATA_DIR = os.path.dirname(PROCESSING_DIR)
sys.path.append(DATA_DIR)
from utils.decide_year import decide_year
from geography.usa.cartography.load_fips_to_state import load_fips_to_state


SHAPEFILE_DIR = os.path.join(
    DATA_DIR,
    "geography",
    "usa",
    "cartography",
    "2022"
)


def convert_fips_to_state(
    gdf: gpd.GeoDataFrame,
    fips_dict: dict
) -> gpd.GeoDataFrame:
    gdf["STATE"] = gdf["STATEFP"].map(fips_dict)
    gdf = gdf.drop(
        columns=["STATEFP"]
    )
    return gdf


def organize_cols(
    gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    gdf = gdf[[
        "STATE",
        "CD118FP",
        "geometry"
    ]]
    gdf = gdf \
        .rename(columns={
            "CD118FP": "DISTRICT",
            "geometry": "GEOMETRY"
        })
    return gdf


def convert_to_geojson(
    gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    gdf["GEOMETRY"] = gdf["GEOMETRY"].apply(
        lambda x:
            gpd.GeoSeries([x]).to_json()
    )
    gdf["GEOMETRY"] = gdf["GEOMETRY"].apply(
        lambda x:
            json.loads(x)["features"][0]["geometry"]
    )
    return gdf


def process_districts(year: str = None):
    if not year:
        year = decide_year(False)
    gdf = gpd.read_file(SHAPEFILE_DIR)
    gdf = convert_fips_to_state(
        gdf,
        load_fips_to_state()
    )
    gdf = organize_cols(gdf)
    gdf = convert_to_geojson(gdf)
    uri, db_name = get_mongo_config()
    upload_df(
        f"{year}_dists",
        uri,
        gdf,
        db_name,
        "overwrite"
    )


if __name__ == "__main__":
    process_districts()
