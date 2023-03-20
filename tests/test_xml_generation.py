import pytest

from main import (
    generate_maps_xml,
    Map,
    make_element_with_children,
    make_next_map_button,
    make_previous_map_button,
    get_map_button_position,
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
    if expected_elem.text != actual_elem.text:
        assert False
    if expected_elem.tail != actual_elem.tail:
        assert False
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
            "onClick": "makeMap",
            "onMouseEnter": f"Test Author {name}",
            "onMouseExit": "clearInfo",
            "position": get_map_button_position(index),
            "width": "40",
            "height": "20",
            "fontSize": "8",
            "color": f"#00000{name}",
        },
    )


def test_map_generation_1():
    actual = generate_maps_xml([make_test_map(1)])

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
    actual = generate_maps_xml([make_test_map(2)])

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
    actual = generate_maps_xml([make_test_map(i) for i in range(8)])

    expected = [
        make_element_with_children(
            "ToggleGroup",
            {"id": "fanMapButtons1", "active": "False"},
            [make_test_map_xml(name=i, index=i) for i in range(8)],
        )
    ]

    assert_xml_lists_equal(actual, expected)


def test_map_generation_len9():
    actual = generate_maps_xml([make_test_map(i) for i in range(9)])

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
    actual = generate_maps_xml([make_test_map(i) for i in range(14)])

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
    actual = generate_maps_xml([make_test_map(i) for i in range(15)])

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
