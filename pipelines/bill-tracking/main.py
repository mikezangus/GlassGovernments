import os
BILL_TRACKING_DIR = os.path.dirname(os.path.abspath(__file__))
STATES_DIR = os.path.join(BILL_TRACKING_DIR, "states")
PA_DIR = os.path.join(STATES_DIR, "pa")
import sys
sys.path.append(PA_DIR)
from run_pa import run_pa


def main():
    run_pa()


if __name__ == "__main__":
    main()
