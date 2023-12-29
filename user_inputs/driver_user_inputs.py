from workflows_user_inputs import year_flow, chamber_flow, state_flow, district_flow, candidate_flow
from utilities_user_inputs import write_start_message


def main(data_source, action):
    year = year_flow(data_source, action)
    chamber_list = chamber_flow(action)
    state_list = state_flow(data_source, action, year, chamber_list)
    district_list = district_flow(data_source, action, year, chamber_list, state_list)
    if data_source.lower() != "internet":
        candidate_list = candidate_flow(action, year, chamber_list, state_list, district_list)
        write_start_message(action = action, year = year, chamber_list = chamber_list, state_list = state_list, district_list = district_list, candidate_list = candidate_list)
        return year, chamber_list, state_list, district_list, candidate_list
    write_start_message(action = action, year = year, chamber_list = chamber_list, state_list = state_list, district_list = district_list)
    return year, chamber_list, state_list, district_list