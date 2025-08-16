from metadata.states.oh.run_oh import run_oh
from metadata.states.pa.run_pa import run_pa
from metadata.states.wi.run_wi import run_wi


def main():
    run_oh()
    run_pa()
    run_wi()


if __name__ == "__main__":
    main()
