import geopandas as gpd
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd

data_file="2022_Deluzio_output.csv"
shapefile="ne_110m_admin_1_states_provinces/ne_110m_admin_1_states_provinces.shp"
data=pd.read_csv(data_file,sep=",")
us_states=gpd.read_file(shapefile)
us_states=us_states[us_states["adm0_a3"] == "USA"]

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

data["state_name"]=data["contributor_state"].map(state_mapping)
state_contributions=dict(zip(data["state_name"],data["total_contribution_amount"]))

colors=cm.get_cmap("Reds")
colors_green=mcolors.LinearSegmentedColormap.from_list("GreenMap",["white","green"],N=256)
normalize=mcolors.Normalize(
    vmin=min(state_contributions.values()),
    vmax=max(state_contributions.values())
)

fig,ax=plt.subplots(1,1,figsize=(10,6))
us_states.boundary.plot(ax=ax)

for idx, row in us_states.iterrows():
    state_name=row["name"]
    if state_name in state_contributions:
        contribution=state_contributions[state_name]
        color=colors(normalize(contribution))
        ax.annotate(
            f"{state_name}\n${contribution:.2f}",
            (row.geometry.centroid.x,row.geometry.centroid.y),
            ha="center",
            va="center",
            fontsize=4,
            color="black",
            bbox=dict(facecolor=color,alpha=0.8)
        )

plt.show()