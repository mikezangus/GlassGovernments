from lxml import html as lxml
from lxml.html import HtmlElement
from shared.utils.normalize_null import normalize_null


def _get_stage_node(doc: HtmlElement, header_text: str) -> HtmlElement | None:
    nodes = doc.xpath(f"//div[@class='group-header'][normalize-space()='{header_text}']/following-sibling::div[1]")
    return nodes[0] if nodes else None


def _extract_fields(section_div: HtmlElement) -> dict[str, str]:
    input_fields = section_div.xpath(
        ".//div[contains(@class,'input-group')]"
        "//div[contains(@class,'input-group-text') and contains(@class,'w-100')]"
    )
    output_fields: dict[str, str] = {}
    for field in input_fields:
        label = normalize_null(' '.join(field.itertext()))
        contents_div = field.xpath("parent::div/following-sibling::div[contains(@class,'form-control')][1]")
        if not contents_div:
            contents_div = field.xpath("parent::div/following-sibling::div[contains(@class,'form-control') and contains(@class,'textarea')][1]")
        contents = normalize_null(' '.join(contents_div[0].itertext())) \
            if contents_div \
            else None
        output_fields[label] = contents
    return output_fields


def extract_raw_actions(html: str) -> list[dict[str, str]]:
    doc: HtmlElement = lxml.fromstring(html)
    nodes = [
        ("lower", _get_stage_node(doc, "House")),
        ("upper", _get_stage_node(doc, "Senate")),
        ("executive", _get_stage_node(doc, "Governor")),
        ("conference & concurrence", _get_stage_node(doc, "Conference & Concurrence")),
        ("veto", _get_stage_node(doc, "Veto")),
        ("enacted", _get_stage_node(doc, "Effective Date"))
    ]
    raw_actions = {}
    for stage, node in nodes:
        raw_actions[stage] = _extract_fields(node) if node is not None else {}
    return raw_actions
