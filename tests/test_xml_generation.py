import pytest

from main import (
    generate_maps_xml,
    Map,
    make_element_with_children,
    MAP_BUTTON_POSITIONS,
)
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


def test_map_generation_1():
    actual = generate_maps_xml([make_test_map(1)])

    expected = [
        make_element_with_children(
            "ToggleGroup",
            {"id": "fanMapButtons1", "active": "False"},
            [
                make_element_with_children(
                    "Button",
                    {
                        "id": "Test Map 1",
                        "onClick": "makeMap",
                        "onMouseEnter": "Test Author 1",
                        "onMouseExit": "clearInfo",
                        "position": "-25 5 -20",
                        "width": "40",
                        "height": "20",
                        "fontSize": "8",
                        "color": "#000001",
                    },
                )
            ],
        )
    ]

    assert xml_lists_equal(actual, expected)


def test_map_generation_2():
    actual = generate_maps_xml([make_test_map(2)])

    expected = [
        make_element_with_children(
            "ToggleGroup",
            {"id": "fanMapButtons1", "active": "False"},
            [
                make_element_with_children(
                    "Button",
                    {
                        "id": "Test Map 2",
                        "onClick": "makeMap",
                        "onMouseEnter": "Test Author 2",
                        "onMouseExit": "clearInfo",
                        "position": "-25 5 -20",
                        "width": "40",
                        "height": "20",
                        "fontSize": "8",
                        "color": "#000002",
                    },
                )
            ],
        )
    ]

    assert xml_lists_equal(actual, expected)


def test_map_generation_len8():
    actual = generate_maps_xml([make_test_map(i) for i in range(1, 9)])

    expected = [
        make_element_with_children(
            "ToggleGroup",
            {"id": "fanMapButtons1", "active": "False"},
            [
                make_element_with_children(
                    "Button",
                    {
                        "id": f"Test Map {i}",
                        "onClick": "makeMap",
                        "onMouseEnter": f"Test Author {i}",
                        "onMouseExit": "clearInfo",
                        "position": MAP_BUTTON_POSITIONS[i - 1],
                        "width": "40",
                        "height": "20",
                        "fontSize": "8",
                        "color": f"#00000{i}",
                    },
                )
                for i in range(1, 9)
            ],
        )
    ]

    assert xml_lists_equal(actual, expected)
