from bs4 import BeautifulSoup, Tag


def _is_valid_row(row: Tag) -> bool:
    if "subheader" in row.get("class", []):
        return False
    cell1 = row.find("div")
    if not cell1 or not cell1.find('a'):
        return False
    return True


def fetch_raw_metadata(html: str) -> list[str]:
    bs = BeautifulSoup(html, "html.parser")
    rows: list[str] = []
    for row in bs.select("div.header ~ div"):
        if not _is_valid_row(row):
            continue
        cells = row.find_all("div", recursive=False)
        text = cells[0].get_text(" ", strip=True)
        if text:
            rows.append(text)
    return rows
