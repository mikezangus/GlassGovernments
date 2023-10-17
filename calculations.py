import geopandas as gpd
import json
import os
import pandas as pd
import streamlit as st
from pymongo import MongoClient
from shapely.geometry import Point

st.markdown("""
    <style>
        .btn-primary {
            color: white;
            background-color: #FF2E63;
        }
        
        .btn-primary.active {
            background-color: green !important;
        }
    </style>
""", unsafe_allow_html=True)


st.title("Who Funded PA District 17's Congressional Candidates in 2022?")


base_directory = "/Users/zangus/Documents/Projects/Project_CREAM"
with open(os.path.join(base_directory, "config.json"), "r") as file:
    config = json.load(file)
config["uri"] = f"mongodb+srv://{config['mongoUsername']}:{config['mongoPassword']}@{config['mongoCluster']}.px0sapn.mongodb.net/{config['mongoDatabase']}?retryWrites=true&w=majority"
client = MongoClient(config["uri"])
db = client[config["mongoDatabase"]]
collection = db["2022_PA"]

unique_names = collection.distinct("candidate_last_name")
candidate_last_name = st.selectbox("Choose candidate:", unique_names)
unique_entities = collection.distinct("entity_type_desc")

st.subheader("Filter per funding entity:")
if 'selected_entities' not in st.session_state:
    st.session_state.selected_entities = unique_entities


MAX_BUTTONS_PER_ROW = 4

num_rows = -(-len(unique_entities) // MAX_BUTTONS_PER_ROW)  # This is a way to calculate the ceiling of a division

for i in range(num_rows):
    start_idx = i * MAX_BUTTONS_PER_ROW
    end_idx = start_idx + MAX_BUTTONS_PER_ROW
    entities_in_row = unique_entities[start_idx:end_idx]
    columns = st.columns(len(entities_in_row))
    for col, entity in zip(columns, entities_in_row):
        button_label = f"{'✅ ' if entity in st.session_state.selected_entities else ''}{entity}"
        if col.button(button_label, key=f"{entity}_{i}"):
            if entity in st.session_state.selected_entities:
                st.session_state.selected_entities.remove(entity)
            else:
                st.session_state.selected_entities.append(entity)

districts_gdf = gpd.read_file(os.path.join(base_directory, "census", "cb_2022_us_cd118_500k", "cb_2022_us_cd118_500k.shp"))
state_boundaries_gdf = gpd.read_file(os.path.join(base_directory, "census", "cb_2022_us_state_500k", "cb_2022_us_state_500k.shp"))

district_pa_17_gdf = districts_gdf[(districts_gdf["STATEFP"] == "42") & (districts_gdf["CD118FP"] == "17")]

pennsylvania_gdf = state_boundaries_gdf[state_boundaries_gdf["STATEFP"] == "42"]
pennsylvania_gdf = pennsylvania_gdf.to_crs(district_pa_17_gdf.crs)

donation_records = list(collection.find({"candidate_last_name": candidate_last_name}))

donations_df = pd.DataFrame(donation_records)
geometry = [Point(xy) for xy in zip(donations_df["contributor_location"].str[1], donations_df["contributor_location"].str[0])]
donations_gdf = gpd.GeoDataFrame(donations_df, geometry = geometry)

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

donations_in_pa = gpd.sjoin(donations_gdf, pennsylvania_gdf, how="inner", predicate="within")
donations_in_district = gpd.sjoin(donations_gdf, district_pa_17_gdf, how = "inner", predicate = "within")

total_in_district = donations_in_district["contribution_receipt_amount"].sum()

pipeline = [
    {
        "$match": {
            "candidate_last_name": candidate_last_name,
            "entity_type_desc": {"$in": st.session_state.selected_entities}
        }
    },
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
    total_raised += result["total_amount"]

total_in_pa = donations_in_pa["contribution_receipt_amount"].sum()

st.write(f"Total raised by {candidate_last_name}: ${total_raised:,.2f}")
st.write(f"Total raised by {candidate_last_name} inside their district: ${total_in_district:,.2f}, {((total_in_district/total_raised) * 100):.2f}% of total raised")
st.write(f"Total raised by {candidate_last_name} outside their district: ${total_raised - total_in_district:,.2f}, {(((total_raised - total_in_district) / total_raised) * 100):.2f}% of total raised")
st.write(f"Total raised by {candidate_last_name} inside their state: ${total_in_pa:,.2f}, {((total_in_pa/total_raised) * 100):.2f}% of total raised")
st.write(f"Total raised by {candidate_last_name} outside their state: ${total_raised - total_in_pa:,.2f}, {(((total_raised - total_in_pa) / total_raised) * 100):.2f}% of total raised")

