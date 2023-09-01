import os
import pandas as pd

last_name = "Lee"
year = "2022"

data_file = f"{year}_{last_name}_source.csv"
output_csv_file = f"{year}_{last_name}_output.csv"
output_excel_file = f"{year}_{last_name}_output.xlsx"

data = pd.read_csv(filepath_or_buffer = data_file, sep = ",")
relevant_columns = ["transaction_id", "entity_type", "contributor_state", "contribution_receipt_amount"]
data = data[relevant_columns]

ind_contributions = data[data["entity_type"] == "IND"]
pac_contributions = data[data["entity_type"] == "PAC"]

def perform_aggregation(data,column_name):
    return data.groupby("contributor_state").agg(
        **{f"{column_name}_contribution_count": pd.NamedAgg(column = "transaction_id", aggfunc = "count"),
           f"{column_name}_contribution_amount": pd.NamedAgg(column = "contribution_receipt_amount", aggfunc = "sum")}
    ).reset_index()

state_data = perform_aggregation(data, "total")
ind_data = perform_aggregation(ind_contributions, "ind")
pac_data = perform_aggregation(pac_contributions, "pac")

combined_by_state_contribution = state_data.merge(ind_data, on = "contributor_state", how = "outer").merge(pac_data, on = "contributor_state", how = "outer")
combined_by_state_contribution.fillna(0, inplace = True)

numeric_columns = ["total_contribution_count", "total_contribution_amount",
                   "ind_contribution_count", "ind_contribution_amount",
                   "pac_contribution_count", "pac_contribution_amount"
]
combined_by_state_contribution[numeric_columns] = combined_by_state_contribution[numeric_columns].astype(float)

output_files = [output_csv_file, output_excel_file]
for file in output_files:
    if os.path.exists(file):
        os.remove(file)

combined_by_state_contribution.to_csv(path_or_buf = output_csv_file, index = False)
combined_by_state_contribution.to_excel(excel_writer = output_excel_file, index = False)