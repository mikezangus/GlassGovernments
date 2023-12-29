from workflows_user_inputs import year_flow, chamber_flow, state_flow, district_flow, candidate_flow
from utilities_user_inputs import write_start_message


def main(data_source, action):
    year = year_flow(data_source = data_source, action = action)
    chamber = chamber_flow(action = action)
    state = state_flow(chamber_input = chamber, data_source = data_source, action = action, year = year)
    district = district_flow(data_source = data_source, action = action, year = year, chamber = chamber, state = state)
    if data_source.lower() != "internet":
        candidate = candidate_flow(action = action, year = year, chamber = chamber, state = state, district = district)
        write_start_message(action = action, year = year, chamber = chamber, state = state, district = district, candidate = candidate)
        return year, chamber, state, district, candidate
    write_start_message(action = action, year = year, chamber = chamber, state = state, district = district)
    return year, chamber, state, district