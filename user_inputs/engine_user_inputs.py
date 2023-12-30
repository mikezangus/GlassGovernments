def process_one_candidate(action: str, year: str, chamber: str, state: str, candidate: str, district: str = None):
    if chamber.lower() == "house":
        candidate_str = f"{year}_{chamber}_{state}_{candidate}"
    elif chamber.lower() == "senate":
        candidate_str = f"{year}_{chamber}_{state}_{district}_{candidate}"
    print(candidate_str)
    return candidate_str