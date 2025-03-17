import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, shape


def write_msg(
    df_name: str,
    action: str,
    df: pd.DataFrame | gpd.GeoDataFrame
) -> str:
    msg = f"\n{df_name} DF | Succeeded to {action}\nLength: {len(df):,}\n{df.head()}"
    return msg


def process_conts_df(
    df: pd.DataFrame
) -> gpd.GeoDataFrame:
    df_name = "Contributions"
    df["LOCATION"] = df["LOCATION"].apply(
        lambda x:
            Point(x["coordinates"]) if x is not None else None
    )
    print(write_msg(df_name, "convert locations to points", df))
    gdf = gpd.GeoDataFrame(
        data=df,
        geometry="LOCATION",
        crs="EPSG:4326"
    )
    print(write_msg(df_name, "create Geo DF", gdf))
    return gdf


def process_cands_dists_df(
    cands_df: pd.DataFrame,
    dists_df: pd.DataFrame
) -> gpd.GeoDataFrame:
    df_name = "Candidates-Districts"
    df = pd.merge(
        left=cands_df,
        right=dists_df,
        on=["STATE", "DISTRICT"],
        how="inner"
    )
    print(write_msg(df_name, "merge", df))
    df["GEOMETRY"] = df["GEOMETRY"].apply(
        lambda x:
            shape(x) if x is not None else None
    )
    print(write_msg(df_name, "convert geometries to shapes", df))
    gdf = gpd.GeoDataFrame(
        data=df,
        geometry="GEOMETRY",
        crs="EPSG:4326"
    )
    print(write_msg(df_name, "create Geo DF", gdf))
    return gdf


def perform_point_in_polygon_test(
    conts_gdf: gpd.GeoDataFrame,
    cands_dists_gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    df_name="Point-in-Polygon"
    df = pd.merge(
        left=conts_gdf,
        right=cands_dists_gdf,
        on="CAND_ID",
        how="inner"
    )
    print(write_msg(df_name, "merge", df))
    df["DOMESTIC"] = df.apply(
        lambda row:
            row["LOCATION"].within(
                row["GEOMETRY"]
            ) if row["LOCATION"] is not None and row["GEOMETRY"] else None,
            axis=1
    )
    print(write_msg(df_name, "perform point-in-polygon test", df))
    return df


def process_districtwide_conts(
    cands_df: pd.DataFrame,
    dists_df: pd.DataFrame,
    conts_df: pd.DataFrame
) -> pd.DataFrame:
    conts_gdf = process_conts_df(
        df=conts_df
    )
    cands_dists_gdf = process_cands_dists_df(
        cands_df=cands_df,
        dists_df=dists_df
    )
    pip_gdf = perform_point_in_polygon_test(
        conts_gdf=conts_gdf,
        cands_dists_gdf=cands_dists_gdf
    )
    df = pd.DataFrame(pip_gdf)
    return df
