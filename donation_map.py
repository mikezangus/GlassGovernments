import folium
import geopandas as gpd
import json
import os
import pandas as pd
from folium.features import DivIcon
from folium.plugins import FeatureGroupSubGroup, HeatMap
from pymongo import MongoClient
from shapely.geometry import Point


base_directory = "/Users/zangus/Documents/Projects/Project_CREAM"
counties_gdf = gpd.read_file(os.path.join(base_directory, "census", "cb_2022_us_county_500k", "cb_2022_us_county_500k.shp"))
districts_gdf = gpd.read_file(os.path.join(base_directory, "census", "cb_2022_us_cd118_500k", "cb_2022_us_cd118_500k.shp"))
district_pa_17 = districts_gdf[(districts_gdf["STATEFP"] == "42") & (districts_gdf["CD118FP"] == "17")]

with open(os.path.join(base_directory, "config.json"), "r") as file:
    config = json.load(file)

config["uri"] = f"mongodb+srv://{config['mongoUsername']}:{config['mongoPassword']}@{config['mongoCluster']}.px0sapn.mongodb.net/{config['mongoDatabase']}?retryWrites=true&w=majority"
client = MongoClient(config["uri"])
db = client[config["mongoDatabase"]]
collection = db["2022_PA"]

candidate_name = input("\nWhich candidate's data do you want to map?: ").upper()

records = collection.find({
    "candidate_last_name": f"{candidate_name}",
    "entity_type_desc": {"$ne": "CANDIDATE"}
})
donation_records = list(records)
donations_df = pd.DataFrame(donation_records)

geometry = [Point(xy) for xy in zip(donations_df["contributor_location"].str[1], donations_df["contributor_location"].str[0])]
donations_gdf = gpd.GeoDataFrame(donations_df, geometry = geometry)

joined = gpd.sjoin(donations_gdf, counties_gdf, how = "inner", op = "within")
donation_summary = joined.groupby(["STATEFP", "COUNTYFP"])["contribution_receipt_amount"].sum().reset_index()

merged = counties_gdf.merge(donation_summary, left_on = ["STATEFP", "COUNTYFP"], right_on = ["STATEFP", "COUNTYFP"], how = "left")
merged.fillna(0, inplace = True)

# m1 = folium.Map(location = [40.0, -80.0], zoom_start = 8)

# folium.Choropleth(
#     geo_data = merged,
#     name = "choropleth",
#     data = merged,
#     columns = ["COUNTYFP", "contribution_receipt_amount"],
#     key_on = "feature.properties.COUNTYFP",
#     fill_color = "YlGnBu",
#     fill_opacity = 0.7,
#     line_opacity = 0.2,
#     legend_name = "Donations per county for Chris Deluzio (PA-17)"
# ).add_to(m1)
# folium.GeoJson(
#     district_pa_17,
#     style_function = lambda feature: {
#         "color": "black",  
#         "weight": 2
#     }
# ).add_to(m1)
# m1.save("Deluzio_donations_by_district.html")

m2 = folium.Map(location = [39.8283, -98.5795], zoom_start = 5)
main_group = folium.FeatureGroup(name = "All Entities").add_to(m2)

for entity_type in donations_df["entity_type_desc"].unique():
    if entity_type != "CANDIDATE":
        subgroup = FeatureGroupSubGroup(main_group, name = entity_type)
        m2.add_child(subgroup)

        for _, record in donations_df[donations_df["entity_type_desc"] == entity_type].iterrows():
            location = record.get("contributor_location")
            if location and isinstance(location, list) and len(location) >= 2:
                lat, lon = location
                amount = record.get("contribution_receipt_amount", 1)
                folium.CircleMarker(
                    location = (lat, lon),
                    radius = amount / 200,
                    color = "blue" if record["entity_type_desc"] == "INDIVIDUAL" else "red",
                    weight = 0.5,
                    fill = True,
                    fill_color = "blue" if record["entity_type_desc"] == "INDIVIDUAL" else "red",
                    tooltip = f"${amount}"
                ).add_to(subgroup)

heat_data = []
for record in donation_records:
    location = record.get("contributor_location")
    if location and isinstance(location, list) and len(location) >= 2:
        lat, lon = location
        amount = record.get("contribution_receipt_amount", 1)
        heat_data.extend([[lat, lon]] * int(amount))

folium.GeoJson(
    district_pa_17,
    style_function = lambda feature: {
        "color": "black",  
        "weight": 2,
        "fillColor": "#ADFF2F",
        "fillOpacity": 0.2
    }
).add_to(m2)
HeatMap(heat_data, radius = 20).add_to(m2)
folium.LayerControl(collapsed = False).add_to(m2)
m2.save(f"heatmap_{candidate_name}.html")