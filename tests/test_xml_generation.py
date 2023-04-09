import pytest

from xml_utilities import make_element_with_children
from fan_maps import (
    Map,
    get_map_button_position,
    make_next_map_button,
    make_previous_map_button,
    get_map_elements,
    BUTTON_PROPERTIES,
    REAL_MAPS,
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


def assert_xml_lists_equal(
    actual: list[ElementTree.Element], expected: list[ElementTree.Element]
):
    if len(expected) != len(actual):
        assert False
    for (
        actual_elem,
        expected_elem,
    ) in zip(actual, expected):
        assert_elements_equal(actual_elem, expected_elem)


def assert_elements_equal(actual_elem, expected_elem):
    if expected_elem.tag != actual_elem.tag:
        assert False
    # if expected_elem.text != actual_elem.text: # I think this never applies in tts
    #     assert False
    # if expected_elem.tail != actual_elem.tail:
    #     assert False
    if expected_elem.attrib != actual_elem.attrib:
        assert False
    if len(expected_elem) != len(actual_elem):
        assert False
    for actual_child, expected_child in zip(actual_elem, expected_elem):
        assert_elements_equal(actual_child, expected_child)


def make_test_map_xml(name: int, index: int) -> ElementTree.Element:
    return make_element_with_children(
        "Button",
        {
            "id": f"Test Map {name}",
            "onclick": "makeMap",
            "onMouseEnter": f"Test Author {name}",
            "onMouseExit": "clearInfo",
            "position": get_map_button_position(index),
            "color": f"#00000{name}",
            "icon": f"Test Map {name}",
            **BUTTON_PROPERTIES,
        },
    )


def test_map_generation_1():
    actual = get_map_elements([make_test_map(1)])

    expected = [
        make_element_with_children(
            "ToggleGroup",
            {"id": "fanMapButtons1", "active": "False"},
            [
                make_test_map_xml(name=1, index=0),
            ],
        )
    ]

    assert_xml_lists_equal(actual, expected)


def test_map_generation_2():
    actual = get_map_elements([make_test_map(2)])

    expected = [
        make_element_with_children(
            "ToggleGroup",
            {"id": "fanMapButtons1", "active": "False"},
            [
                make_test_map_xml(name=2, index=0),
            ],
        )
    ]

    assert_xml_lists_equal(actual, expected)


def test_map_generation_len8():
    actual = get_map_elements([make_test_map(i) for i in range(8)])

    expected = [
        make_element_with_children(
            "ToggleGroup",
            {"id": "fanMapButtons1", "active": "False"},
            [make_test_map_xml(name=i, index=i) for i in range(8)],
        )
    ]

    assert_xml_lists_equal(actual, expected)


def test_map_generation_len9():
    actual = get_map_elements([make_test_map(i) for i in range(9)])

    expected = [
        make_element_with_children(
            "ToggleGroup",
            {"id": "fanMapButtons1", "active": "False"},
            [make_test_map_xml(name=i, index=i) for i in range(7)]
            + [make_next_map_button(0)],
        ),
        make_element_with_children(
            "ToggleGroup",
            {"id": "fanMapButtons2", "active": "False"},
            [
                make_test_map_xml(name=7, index=0),
                make_test_map_xml(name=8, index=1),
                make_previous_map_button(1),
            ],
        ),
    ]

    assert_xml_lists_equal(actual, expected)


def test_map_generation__2_full_pages():
    actual = get_map_elements([make_test_map(i) for i in range(14)])

    first_page_buttons = [make_test_map_xml(name=i, index=i) for i in range(7)] + [
        make_next_map_button(0)
    ]

    second_page_buttons = (
        [make_test_map_xml(name=i + 7, index=i) for i in range(4)]
        + [make_previous_map_button(1)]
        + [make_test_map_xml(name=i + 11, index=i + 5) for i in range(3)]
    )

    expected = [
        make_element_with_children(
            "ToggleGroup",
            {"id": "fanMapButtons1", "active": "False"},
            first_page_buttons,
        ),
        make_element_with_children(
            "ToggleGroup",
            {"id": "fanMapButtons2", "active": "False"},
            second_page_buttons,
        ),
    ]

    assert_xml_lists_equal(actual, expected)


def test_map_generation__3_pages():
    actual = get_map_elements([make_test_map(i) for i in range(15)])

    first_page_buttons = [make_test_map_xml(name=i, index=i) for i in range(7)] + [
        make_next_map_button(0)
    ]

    second_page_buttons = (
        [make_test_map_xml(name=i + 7, index=i) for i in range(4)]
        + [make_previous_map_button(1)]
        + [make_test_map_xml(name=i + 11, index=i + 5) for i in range(2)]
        + [make_next_map_button(1)]
    )

    third_page_buttons = [make_test_map_xml(name=i + 13, index=i) for i in range(2)] + [
        make_previous_map_button(2)
    ]

    expected = [
        make_element_with_children(
            "ToggleGroup",
            {"id": "fanMapButtons1", "active": "False"},
            first_page_buttons,
        ),
        make_element_with_children(
            "ToggleGroup",
            {"id": "fanMapButtons2", "active": "False"},
            second_page_buttons,
        ),
        make_element_with_children(
            "ToggleGroup",
            {"id": "fanMapButtons3", "active": "False"},
            third_page_buttons,
        ),
    ]

    assert_xml_lists_equal(actual, expected)


def test_map_generation__real_data():
    actual = get_map_elements(REAL_MAPS)

    expected_xml = [
        """
<ToggleGroup id="fanMapButtons1" active="False">
    <Button id="Summer Map" onclick="makeMap" onMouseEnter = "infoNevakanezahAndSlug" onMouseExit="clearInfo" position="-25 5 -20" width="40" height="20" fontSize="8" icon ="Summer Map" color="#4b4d35"/>
    <Button id="Legends Map" onclick="makeMap" onMouseEnter = "infoSlug" onMouseExit="clearInfo" position="15 5 -20" width="40" height="20" fontSize="8" icon ="Legends Map" color="#FAE5B3"/>
    <Button id="Urban Map" onclick="makeMap" onMouseEnter = "infoSlug" onMouseExit="clearInfo" position="55 5 -20" width="40" height="20" fontSize="8" icon ="Urban Map" color="#9b8551"/>
    <Button id="Lost Woodland Map" onclick="makeMap" onMouseEnter = "infoEndgamer" onMouseExit="clearInfo" position="95 5 -20" width="40" height="20" fontSize="8" icon ="Lost Woodland Map" color="#5b5a36"/>

    <Button id="Gorge Map" onclick="makeMap" onMouseEnter = "infoLordOfTheBoard" onMouseExit="clearInfo" position="-25 -15 -20" width="40" height="20" fontSize="8" icon ="Gorge Map" color="#61746b"/>
    <Button id="Treasure Island Map" onclick="makeMap" position="15 -15 -20" width="40" height="20" onMouseEnter = "infoSupacatone" onMouseExit="clearInfo" fontSize="8" icon ="Treasure Island Map" color="#567826"/>
    <Button id="Deep Woods Map" onclick="makeMap" onMouseEnter="infoSlug" onMouseExit="clearInfo" position="55 -15 -20" width="40" height="20" fontSize="8" icon ="Deep Woods Map" color="#3f4839"/>
    <Button onclick="maps2" position="95 -15 -20" width="40" height="20" fontSize="8" icon ="More Button" color="#f3ecd1"/>
</ToggleGroup>""",
        """
<ToggleGroup id="fanMapButtons2" active="False">
  <Button id="Australia Map" onclick="makeMap" onMouseEnter = "infoVatechman3" onMouseExit="clearInfo" position="-25 5 -20" width="40" height="20" fontSize="8" icon ="Australia Map" color="#899c58"/>
  <Button id="Narrows and Islets Map" onclick="makeMap" onMouseEnter = "infoHierotitanAndLeonatus" onMouseExit="clearInfo" position="15 5 -20" width="40" height="20" fontSize="8" icon ="Narrows and Islets Map" color="#9c9a7b"/>
  <Button id="Tunnel Unraveled Map" onclick="makeMap" onMouseEnter = "infoTunnelMap" onMouseExit="clearInfo" position="55 5 -20" width="40" height="20" fontSize="8" icon ="Tunnel Unraveled Map" color="#422e19"/>
  <Button id="Tropics Map" onclick="makeMap" onMouseEnter = "infoJ444" onMouseExit="clearInfo" position="95 5 -20" width="40" height="20" fontSize="8" icon ="Tropics Map" color="#7e986c"/>
  
  <Button onclick="maps1" position="-25 -15 -20" width="40" height="20" fontSize="8" icon ="Back Button" color="#f3ecd1"/>
  <Button id="Wastelands Map" onclick="makeMap" onMouseEnter = "infoSlug" onMouseExit="clearInfo" position="15 -15 -20" width="40" height="20" fontSize="8" icon ="Wastelands Map" color="#83805b"/>  
</ToggleGroup>""",
    ]
    expected_elements = [ElementTree.fromstring(xml) for xml in expected_xml]

    assert_xml_lists_equal(actual, expected_elements)
