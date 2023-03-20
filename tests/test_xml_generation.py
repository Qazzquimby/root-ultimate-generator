import pytest

from main import generate_maps_xml, Map, make_element_with_children
import xml.etree.ElementTree as ElementTree

# target_xml = Path("tests/target.xml").read_text()
#
# def test_xml_generation():
#     assert generate_faction_selector() == target_xml


def make_test_map(index: int) -> Map:
    return Map(
        name=f"Test Map {index}", author=f"Test Author {index}", color=f"#00000{index}"
    )


def xml_lists_equal(xml1: list[ElementTree.Element], xml2: list[ElementTree.Element]):
    if len(xml1) != len(xml2):
        return False
    return all(elements_equal(e1, e2) for e1, e2 in zip(xml1, xml2))


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
    "indices, expected",
    [
        (
            [1],
            [
                make_element_with_children(
                    "ToggleGroup",
                    {"id": "fanMapButtons1", "active": "False"},
                    [
                        make_element_with_children(
                            "Test Map 1",
                            {"author": "Test Author 1", "color": "#000001"},
                        )
                    ],
                )
            ],
        ),
        (
            [2],
            [
                make_element_with_children(
                    "ToggleGroup",
                    {"id": "fanMapButtons1", "active": "False"},
                    [
                        make_element_with_children(
                            "Test Map 2",
                            {"author": "Test Author 2", "color": "#000002"},
                        )
                    ],
                )
            ],
        ),
        (
            [3, 4],
            [
                make_element_with_children(
                    "ToggleGroup",
                    {"id": "fanMapButtons1", "active": "False"},
                    [
                        make_element_with_children(
                            "Test Map 3",
                            {"author": "Test Author 3", "color": "#000003"},
                        ),
                        make_element_with_children(
                            "Test Map 4",
                            {"author": "Test Author 4", "color": "#000004"},
                        ),
                    ],
                )
            ],
        ),
    ],
)
def test_map_generation(indices: list[int], expected):
    actual = generate_maps_xml([make_test_map(index) for index in indices])

    assert xml_lists_equal(actual, expected)
