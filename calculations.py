import geopandas as gpd
import json
import os
import pandas as pd
from pymongo import MongoClient
from shapely.geometry import Point

base_directory = "/Users/zangus/Documents/Projects/Project_CREAM"
with open(os.path.join(base_directory, "config.json"), "r") as file:
    config = json.load(file)

config["uri"] = f"mongodb+srv://{config['mongoUsername']}:{config['mongoPassword']}@{config['mongoCluster']}.px0sapn.mongodb.net/{config['mongoDatabase']}?retryWrites=true&w=majority"

client = MongoClient(config["uri"])
db = client[config["mongoDatabase"]]
collection = db["2022_PA"]

candidate_last_name = input("\nWhich candidate do you want to calculate?: ").upper()

districts_gdf = gpd.read_file(os.path.join(base_directory, "census", "cb_2022_us_cd118_500k", "cb_2022_us_cd118_500k.shp"))
district_pa_17_gdf = districts_gdf[(districts_gdf["STATEFP"] == "42") & (districts_gdf["CD118FP"] == "17")]



donation_records = list(collection.find({"candidate_last_name": candidate_last_name}))



donations_df = pd.DataFrame(donation_records)
geometry = [Point(xy) for xy in zip(donations_df["contributor_location"].str[1], donations_df["contributor_location"].str[0])]
donations_gdf = gpd.GeoDataFrame(donations_df, geometry = geometry)


import matplotlib.pyplot as plt
district_pa_17_gdf.boundary.plot(color='blue', linewidth=1.5, figsize=(10,10))
plt.title("PA-17 District Boundary and Donations for DELUZIO")
donations_gdf.plot(marker='o', color='red', markersize=5, ax=plt.gca())
plt.show()


def generate_point(row):
    try:
        location = row["contributor_location"]
        lon = float(location[1])
        lat = float(location[0])
        return Point(lon, lat)
    except:
        return None

donations_df["geometry"] = donations_df.apply(generate_point, axis = 1)

donations_gdf = donations_gdf.set_crs(district_pa_17_gdf.crs)

donations_in_district = gpd.sjoin(donations_gdf, district_pa_17_gdf, how = "inner", predicate = "within")

total_in_district = donations_in_district["contribution_receipt_amount"].sum()


pipeline = [
    {"$match": {"candidate_last_name": candidate_last_name}},
    {
        "$group": {
            "_id": "$entity_type_desc",
            "total_amount": {"$sum": "$contribution_receipt_amount"}
        }
    },
    {
        "$sort": {"total_amount": -1}
    }
]

results = list(collection.aggregate(pipeline))
total_raised = 0
for result in results:
    entity_type = result["_id"]
    amount = result["total_amount"]
    total_raised += amount
    print(f"Entity type: {entity_type} | Total raised: ${amount:,.2f}")
print(f"Total raised by {candidate_last_name}: ${total_raised:,.2f}")
print(f"Total raised by {candidate_last_name} inside the district: ${total_in_district:,.2f}")
print(f"Total raised by {candidate_last_name} outside the district: ${total_raised - total_in_district:,.2f}")