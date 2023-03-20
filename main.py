from pathlib import Path
import xml.etree.ElementTree as ElementTree
from xml.etree import ElementTree as ElementTree

import pydantic

template = Path("xml_template.xml").read_text()


def generate_faction_selector():
    return template  # todo


class Map(pydantic.BaseModel):
    name: str
    author: str
    color: str


MAP_BUTTON_POSITIONS = [
    "-25 5 -20",
    "15 5 -20",
    "55 5 -20",
    "95 5 -20",
    "-25 -15 -20",
    "15 -15 -20",
    "55 -15 -20",
    "95 -15 -20",
]


def get_map_button_position(index: int):
    return MAP_BUTTON_POSITIONS[index % len(MAP_BUTTON_POSITIONS)]


def make_element_with_children(
    name: str, attributes: dict[str, str], children: list[ElementTree.Element] = None
) -> ElementTree.Element:
    if children is None:
        children = []

    element = ElementTree.Element(name, attributes)
    for child in children:
        element.append(child)
    return element


# <Button onclick="maps2" position="95 -15 -20" width="40" height="20" fontSize="8" icon ="More Button" color="#f3ecd1"/>
def make_next_map_button(current_page: int):
    return make_element_with_children(
        "Button",
        {
            "onclick": f"maps{current_page + 1}",
            "position": MAP_BUTTON_POSITIONS[-1],
            "width": "40",
            "height": "20",
            "fontSize": "8",
            "icon": "More Button",
            "color": "#f3ecd1",
        },
    )


def make_previous_map_button(current_page: int):
    return make_element_with_children(
        "Button",
        {
            "onclick": f"maps{current_page - 1}",
            "position": MAP_BUTTON_POSITIONS[4],
            "width": "40",
            "height": "20",
            "fontSize": "8",
            "icon": "Back Button",
            "color": "#f3ecd1",
        },
    )


def generate_maps_xml(maps: list[Map]):
    xml = [
        make_element_with_children(
            "ToggleGroup",
            {"id": "fanMapButtons1", "active": "False"},
            [
                make_element_with_children(
                    "Button",
                    {
                        "id": _map.name,
                        "onClick": "makeMap",
                        "onMouseEnter": _map.author,
                        "onMouseExit": "clearInfo",
                        "position": get_map_button_position(index),
                        "width": "40",
                        "height": "20",
                        "fontSize": "8",
                        "color": _map.color,
                    },
                )
                for index, _map in enumerate(maps)
            ],
        )
    ]

    return xml
