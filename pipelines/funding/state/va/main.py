import os
import xml.etree.ElementTree as ET
from collections import Counter


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.dirname(CURRENT_DIR)
FUNDING_DIR = os.path.dirname(STATE_DIR)
PIPELINES_DIR = os.path.dirname(FUNDING_DIR)
PROJECT_DIR = os.path.dirname(PIPELINES_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data", "funding", "state", "va", "2025")


SEARS_FILE_PATH = os.path.join(DATA_DIR, "sears_2024-12-31_2024-09-04.xml")
SPANBERGER_FILE_PATH = os.path.join(DATA_DIR, "spanberger_2024-12-31_2024-07-01.xml")


def main():
    tree = ET.parse(SPANBERGER_FILE_PATH)
    root = tree.getroot()
    ns = { "ns": "http://www.sbe.virginia.gov" }
    schedula_a = root.find("ns:ScheduleA", namespaces=ns)
    results = []
    for lia in schedula_a.findall("ns:LiA", namespaces=ns):
        contributor_element = lia.find("ns:Contributor", namespaces=ns)
        address_element = contributor_element.find("ns:Address", namespaces=ns)
        state_element = address_element.find("ns:State", namespaces=ns)
        amount_element = lia.find("ns:Amount", namespaces=ns)
        date_element = lia.find("ns:TransactionDate", namespaces=ns)

        is_individual = contributor_element.attrib.get("IsIndividual", None)
        state = state_element.text if state_element is not None else None
        amount = amount_element.text if amount_element is not None else None
        date = date_element.text if date_element is not None else None

        results.append({
            "is_individual": is_individual,
            "state": state,
            "amount": amount,
            "date": date
        })

    # results_len = len(results)
    # print(results)
    state_counts = Counter(entry["state"] for entry in results)
    is_individual_counts = Counter(entry["is_individual"] for entry in results)
    print("\nState counts:\n", state_counts)
    print("\nIs individual counts:\n", is_individual_counts)

if __name__ == "__main__":
    main()
