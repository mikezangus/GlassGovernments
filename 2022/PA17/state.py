import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

shapefile = "ne_110m_admin_1_states_provinces/ne_110m_admin_1_states_provinces.shp"
us_states = gpd.read_file(shapefile)
us_states = us_states[us_states["adm0_a3"] == "USA"]
print(us_states.head())

state_numbers = {"Pennsylvania": 69, "Ohio": 420}

fig, ax = plt.subplots(1, 1, figsize = (10, 6))
us_states.boundary.plot(ax = ax)

for idx, row in us_states.iterrows():
    state_name = row["name"]
    if state_name in state_numbers:
        number = state_numbers[state_name]
        ax.annotate(number, (row.geometry.centroid.x, row.geometry.centroid.y), ha = "center", va = "center", fontsize = 8, color = "black")

plt.show()