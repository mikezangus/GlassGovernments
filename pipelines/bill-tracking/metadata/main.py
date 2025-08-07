from states.oh.run_oh import run_oh
from states.pa.run_pa import run_pa
from states.wi.run_wi import run_wi


def main():
    run_wi()
    run_oh()
    run_pa()


if __name__ == "__main__":
    main()