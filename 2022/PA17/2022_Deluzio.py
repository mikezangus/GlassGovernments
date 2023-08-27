import geopandas as gpd
import matplotlib.pyplot as plt
import os
import pandas as pd

data_file = "2022/PA17/2022_Deluzio_source.csv"
output_csv_file = "2022/PA17/2022_Deluzio_output.csv"
output_excel_file = "2022/PA17/2022_Deluzio_output.xlsx"

data = pd.read_csv(filepath_or_buffer = data_file, sep = ",")
relevant_columns = ["transaction_id", "entity_type", "contributor_state", "contribution_receipt_amount"]
data = data[relevant_columns]

ind_contributions = data[data["entity_type"] == "IND"]
pac_contributions = data[data["entity_type"] == "PAC"]

def perform_aggregation(data, column_name):
    return data.groupby("contributor_state").agg(
        **{f"{column_name}_contribution_count": pd.NamedAgg(column = "transaction_id", aggfunc = "count"),
           f"{column_name}_contribution_amount": pd.NamedAgg(column = "contribution_receipt_amount", aggfunc = "sum")}
    ).reset_index()

state_data = perform_aggregation(data, "total")
ind_data = perform_aggregation(ind_contributions, "ind")
pac_data = perform_aggregation(pac_contributions, "pac")

combined_by_state_contribution = state_data.merge(ind_data, on = "contributor_state", how = "outer").merge(pac_data, on = "contributor_state", how = "outer")
combined_by_state_contribution.fillna(0, inplace = True)

output_files = [output_csv_file, output_excel_file]
for file in output_files:
    if os.path.exists(file):
        os.remove(file)

combined_by_state_contribution.to_csv(path_or_buf = output_csv_file, index = False)
combined_by_state_contribution.to_excel(excel_writer = output_excel_file, sheet_name = "by_state", index = False)

shapefile = "ne_110m_admin_1_states_provinces/ne_110m_admin_1_states_provinces.shp"
data_file = "2022/PA17/2022_Deluzio_output.csv"
data = pd.read_csv(data_file, sep = ",")

state_mapping = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
                 "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida",
                 "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana",
                 "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine",
                 "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
                 "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire",
                 "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota",
                 "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island",
                 "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
                 "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin",
                 "WY": "Wyoming"}

data["state_name"] = data["contributor_state"].map(state_mapping)
state_contributions = dict(zip(data["state_name"], data["total_contribution_amount"]))
us_states = gpd.read_file(shapefile)
us_states = us_states[us_states["adm0_a3"] == "USA"]

fig, ax = plt.subplots(1, 1, figsize = (10, 6))
us_states.boundary.plot(ax = ax)

for idx, row in us_states.iterrows():
    state_name = row["name"]
    if state_name in state_contributions:
        contribution = state_contributions[state_name]
        ax.annotate(f"{state_name}\n${contribution:.2f}", (row.geometry.centroid.x, row.geometry.centroid.y), ha = "center", va = "center", fontsize = 8, color = "black")

plt.show()