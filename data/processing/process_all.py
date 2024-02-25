from process_candidates import main as process_candidates
from process_contributions import main as process_contributions
from modules.decide_year import decide_year


def main():
    year = decide_year()
    process_candidates(year)
    process_contributions(year)
    return


if __name__ == "__main__":
    main()
