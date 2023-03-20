from pathlib import Path

from main import generate_faction_selector

target_xml = Path("tests/target.xml").read_text()

def test_xml_generation():
    assert generate_faction_selector() == target_xml