import json
from pathlib import Path

from fan_maps import get_map_elements, REAL_MAPS
from save_builder import build_xml


def test_escape_xml():
    # todo this is unused becauase no escaping is needed
    expected = '<Button id="xButton" onclick="deleteThis" position="117 85 -15" width="15" height="15" fontSize="8" padding="4 4 4" icon = "Xmark" color="#bd2608" active="false"/>\r\n<Image id="info" image="Blank Info" position="35 -85 -20" width="156" height="6"/>\r\n<Image id="rootLogo" position="-87.5 80 -20" width="75" height="25" image="Root Logo"/>'
    _input = """<Button id="xButton" onclick="deleteThis" position="117 85 -15" width="15" height="15" fontSize="8" padding="4 4 4" icon = "Xmark" color="#bd2608" active="false"/>
<Image id="info" image="Blank Info" position="35 -85 -20" width="156" height="6"/>
<Image id="rootLogo" position="-87.5 80 -20" width="75" height="25" image="Root Logo"/>"""

    actual = _input

    expected = expected.replace("\r", "").replace("\n", "")
    actual = actual.replace("\r", "").replace("\n", "")

    assert expected == actual


def test_with_real_maps():
    real_maps_xml = get_map_elements(REAL_MAPS)
    actual = build_xml(real_maps_xml)
    actual = actual.replace("\r", "").replace("\n", "")
    # string escape actual.
    # '<Button id="xButton" ...
    # -> '"<Button id=\\"XButton\\" ...
    # use built in escape function
    escaped_actual = json.dumps(actual)

    expected = Path("data/real_xml.txt").read_text()
    expected = (
        expected.replace("\r", "")
        .replace("\n", "")
        .replace(r"\r", "")
        .replace(r"\n", "")
    )

    # not a useful test either.
    # pretty hard to test this because order and whitespace could happily differ.
    # also the file is huge
    assert escaped_actual == expected
