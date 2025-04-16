import os
import xml.etree.ElementTree as ET


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.dirname(CURRENT_DIR)
FUNDING_DIR = os.path.dirname(STATE_DIR)
PIPELINES_DIR = os.path.dirname(FUNDING_DIR)
PROJECT_DIR = os.path.dirname(PIPELINES_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data", "funding", "state", "va", "2025")


SEARS_FILE_PATH = os.path.join(DATA_DIR, "sears_2024-12-31_2024-09-04.xml")


def main():
    tree = ET.parse(SEARS_FILE_PATH)
    root = tree.getroot()
    ns = { "ns": "http://www.sbe.virginia.gov" }
    schedula_a = root.find("ns:ScheduleA", namespaces=ns)
    for lia in schedula_a.findall("ns:LiA", namespaces=ns):
        amount_element = lia.find("ns:Amount", namespaces=ns)
        amount = amount_element.text
        print(amount)


if __name__ == "__main__":
    main()