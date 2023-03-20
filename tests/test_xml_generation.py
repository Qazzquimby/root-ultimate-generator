from pathlib import Path

import pydantic as pydantic
import pytest

from main import generate_faction_selector, generate_maps_xml, Map
import xml.etree.ElementTree as ElementTree

# target_xml = Path("tests/target.xml").read_text()
#
# def test_xml_generation():
#     assert generate_faction_selector() == target_xml


def make_test_map(index: int) -> Map:
    return Map(
        name=f"Test Map {index}", author=f"Test Author {index}", color=f"#00000{index}"
    )


def elements_equal(e1, e2):
    if e1.tag != e2.tag:
        return False
    if e1.text != e2.text:
        return False
    if e1.tail != e2.tail:
        return False
    if e1.attrib != e2.attrib:
        return False
    if len(e1) != len(e2):
        return False
    return all(elements_equal(c1, c2) for c1, c2 in zip(e1, e2))


@pytest.mark.parametrize(
    "indices",
    [
        [1],
        # [2],
    ],
)
def test_map_generation(indices: list[int]):

    actual = generate_maps_xml([make_test_map(index) for index in indices])

    # <ToggleGroup id="fanMapButtons1" active="False">
    #     f"Test Map 1", {"author": "Test Author 1", "color": "#000001"}
    expected = ElementTree.Element(
        "ToggleGroup", {"id": "fanMapButtons1", "active": "False"}
    )
    expected.append(
        ElementTree.Element(
            "Test Map 1", {"author": "Test Author 1", "color": "#000001"}
        )
    )

    assert elements_equal(actual, expected)
