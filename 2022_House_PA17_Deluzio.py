import pandas as pd

data_file = "2022_House_PA17_Deluzio.csv"
data = pd.read_csv(filepath_or_buffer = data_file, sep = ",")

relevant_columns = ["transaction_id", "entity_type", "contributor_name", "contributor_first_name", "contributor_last_name", "contributor_street_1",
                    "contributor_city", "contributor_state", "contributor_zip", "contribution_receipt_date", "contribution_receipt_amount"]
data = data[relevant_columns]
individual_data = data[data["entity_type"] == "IND"]
pac_data = data[data["entity_type"] == "PAC"]

def format_with_commas(number):
    return "{:,}".format(number)

total_contribution_count = data["transaction_id"].count()
total_contribution_amount = data["contribution_receipt_amount"].sum()
total_individual_contribution_count = individual_data["transaction_id"].count()
total_individual_contribution_amount = individual_data["contribution_receipt_amount"].sum()
total_pac_contribution_count = pac_data["transaction_id"].count()
total_pac_contribution_amount = pac_data["contribution_receipt_amount"].sum()

print("Total Contribution Count: " + format_with_commas(total_contribution_count), "Total Contribution Amount: $" + format_with_commas(total_contribution_amount),
      "Total Individual Contribution Count: " + format_with_commas(total_individual_contribution_count), "Total Individual Contribution Amount: $" + format_with_commas(total_individual_contribution_amount),
      "Total PAC Contribution Count: " + format_with_commas(total_pac_contribution_count), "Total PAC Contribution Amount: $" + format_with_commas(total_pac_contribution_amount), sep = "\n")


by_state_contribution_count = data.groupby("contributor_state")["transaction_id"].count().reset_index()
by_state_contribution_count = by_state_contribution_count.rename(columns = {"transaction_id": "contribution_count"})
by_state_contribution_count = by_state_contribution_count.sort_values(by = "contribution_count", ascending = False)
by_state_contribution_count["contribution_count_percentage"] = (by_state_contribution_count["contribution_count"] / total_contribution_count) * 100
by_state_contribution_count["contribution_count_percentage"] = by_state_contribution_count["contribution_count_percentage"].apply(lambda x: "{:.2f}%".format(x))

by_state_contribution_amount = data.groupby("contributor_state")["contribution_receipt_amount"].sum().reset_index()
by_state_contribution_amount = by_state_contribution_amount.rename(columns = {"contribution_receipt_amount": "contribution_amount"})
by_state_contribution_amount = by_state_contribution_amount.sort_values(by = "contribution_amount", ascending = False)
by_state_contribution_amount["contribution_amount"] = (by_state_contribution_amount["contribution_amount"].apply(lambda x: "${:,.2f}".format(x)))
by_state_contribution_amount["contribution_amount_percentage"] = (by_state_contribution_amount["contribution_amount"].str.replace("$", "").str.replace(",", "").astype(float) / total_contribution_amount) * 100
by_state_contribution_amount["contribution_amount_percentage"] = by_state_contribution_amount["contribution_amount_percentage"].apply(lambda x: "{:.2f}%".format(x))

combined_by_state_contribution = by_state_contribution_count.merge(by_state_contribution_amount, on = "contributor_state", how = "outer").fillna(0)
print(combined_by_state_contribution)




# individual_state_contribution = individual_data.groupby("contributor_state")["contribution_receipt_amount"].sum().reset_index()
# individual_state_contribution = individual_state_contribution.rename(columns = {"contribution_receipt_amount": "total_individual_contribution_amount"})


# pac_state_contribution = pac_data.groupby("contributor_state")["contribution_receipt_amount"].sum().reset_index()
# pac_state_contribution = pac_state_contribution.rename(columns = {"contribution_receipt_amount": "total_pac_contribution_amount"})

# merged_state_contribution = individual_state_contribution.merge(pac_state_contribution, on = "contributor_state", how = "outer").fillna(0)
# merged_state_contribution["individual_contribution_percentage"] = (merged_state_contribution["total_individual_contribution_amount"] / total_individual_contributions) * 100
# merged_state_contribution["pac_contribution_percentage"] = (merged_state_contribution["total_pac_contribution_amount"] / total_pac_contributions) * 100

# print(merged_state_contribution)


# state_contributions_count = data.groupby("contributor_state")["transaction_id"].count().reset_index()
# state_contributions_count = state_contributions_count.rename(columns = {"transaction_id": "contribution_count"})
# print(state_contributions_count)

# state_contributions_money = data.groupby("contributor_state")["contribution_receipt_amount"].sum().reset_index()
# state_contributions_money = state_contributions_money.rename(columns = {"contribution_receipt_amount": "contribution_amount"})
# print(state_contributions_money)

# total_contributions_amount = data["contribution_receipt_amount"].sum()
# state_contribution_amounts = data.groupby("contributor_state")["contribution_receipt_amount"].sum().reset_index()
# state_contribution_amounts = state_contribution_amounts.rename(columns = {"contribution_receipt_amount": "total_contribution_amount"})

# state_contribution_amounts["contribution_percentage"] = (state_contribution_amounts["total_contribution_amount"] / total_contributions_amount) * 100

# print(state_contribution_amounts)