from bs4 import BeautifulSoup


def extract_text_from_html(html: str) -> str:
    bs = BeautifulSoup(html, "html.parser")
    text_divs = bs.find_all("div", class_=lambda c: c and c.startswith("t "))
    line_numbers = {}
    for div in text_divs:
        if div.has_attr("data-islnnbr") and div["data-islnnbr"] == "true":
            line_id = div.get("id")
            line_text = div.get_text(strip=True)
            line_numbers[line_id] = line_text
    lines = []
    for div in text_divs:
        if not (div.has_attr("data-islnnbr") and div["data-islnnbr"] == "true"):
            text = div.get_text(strip=True)
            line_ref = div.get("data-ln-ref")
            if line_ref and line_ref in line_numbers:
                number = line_numbers[line_ref]
                lines.append(f"{number} {text}")
            else:
                lines.append(text)
    return "\n".join(lines)
