from datetime import datetime
from html import unescape as html_unescape
from lxml import html as lxml
from lxml.html import HtmlElement
from shared.lib.regexes import committee_regex
from shared.utils.normalize_space import normalize_space


def _get_fa_token(icon_classes: str) -> str | None:
    for icon_class in icon_classes.split():
        if icon_class.startswith("fa-") and icon_class != "fas":
            return icon_class
    return None


def _get_stage_chamber(span: HtmlElement, fa_token: str | None) -> str | None:
    if fa_token == "fa-pen-fancy":
        return "executive"
    texts = span.xpath("./strong/text()")
    if not texts:
        return None
    marker = "".join(texts).strip()
    if not marker:
        return None
    match marker.upper():
        case 'H': return "lower"
        case 'S': return "upper"
    return None
    

def _parse_description(p: HtmlElement) -> str:
    nodes = p.xpath("./br/following-sibling::text()")
    description = ""
    for node in nodes:
        chunk = normalize_space(node)
        if chunk:
            if description:
                description += ""
            description += chunk
    return description


def _parse_committee(p: HtmlElement) -> str | None:
    text = "".join(p.itertext()).strip()
    if not text:
        return None
    match = committee_regex.search(text)
    return match.group(1).strip() if match else None
    

def _parse_action_details(fragment: HtmlElement, committee_stage: bool = False) -> list[dict]:
    details = []
    p_nodes = fragment.xpath('.//div[contains(@class,"text-start")]//p')
    for p in p_nodes:
        date = p.text
        if date:
            date = datetime.strptime(date, "%m/%d/%Y").date().isoformat()
        description = _parse_description(p)
        committee = None
        if committee_stage:
            committee = _parse_committee(p)
        if committee:
            committee = normalize_space(committee.lower())
        details.append({
            "date": date,
            "description": normalize_space(description),
            "committee": committee,
        })
    return details


def _parse_stage_actions(stage_span: HtmlElement, key: str) -> list[dict]:
    actions = []
    stage_element = (
        stage_span.get("title") or
        stage_span.get("aria-label") or
        stage_span.get("data-bs-original-title")
    )
    if not stage_element:
        return None
    stage_fragement = lxml.fromstring(html_unescape(stage_element))
    action_details = _parse_action_details(stage_fragement, key.endswith("committee"))
    for action_detail in action_details:
        actions.append({
            "date": action_detail["date"],
            "description": action_detail["description"],
            "committee": action_detail["committee"]
        })
    return actions


def parse_actions(html: str) -> list[dict]:
    actions: list[dict] = []
    icon_map = {
        "fa-inbox-in": "referred_to_committee",
        "fa-inbox-out": "reported_from_committee",
        "fa-thumbs-up": "third_consideration_passed",
        "fa-pen-fancy": "executive_action"
    }
    doc = lxml.fromstring(html)
    stage_spans = doc.xpath(
        '//div[contains(@class,"timeline timeline-big")]'
        '//div[contains(@class,"timeline-Element") or contains(@class,"timeline-Element-Spacer")]'
        '/span'
    )
    chamber = None
    for stage_span in stage_spans:
        icon_classes = " ".join(stage_span.xpath(".//i/@class"))
        fa_token = _get_fa_token(icon_classes)
        stage_chamber = _get_stage_chamber(stage_span, fa_token)
        if stage_chamber is not None:
            chamber = stage_chamber
        key = icon_map.get(fa_token, "")
        stage_actions = _parse_stage_actions(stage_span, key)
        for stage_action in stage_actions:
            actions.append({
                "key": key,
                "chamber": chamber,
                "date": stage_action["date"],
                "description": stage_action["description"],
                "committee": stage_action["committee"]
            })
    return actions
