from file_types.candidates import process_candidates
from file_types.committee_contributions import process_committee_contributions
from file_types.individual_contributions import process_individual_contributions
from file_types.other_contributions import process_other_contributions
from modules.decide_year import decide_year


def main():
    year = decide_year()
    process_candidates(year)
    process_committee_contributions(year)
    process_individual_contributions(year)
    process_other_contributions(year)
    return


if __name__ == "__main__":
    main()
