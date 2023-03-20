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
                        "position": "-25 5 -20",
                        "width": "40",
                        "height": "20",
                        "fontSize": "8",
                        "color": _map.color,
                    },
                )
                for _map in maps
            ],
        )
    ]

    return xml


# jinja template is named for an xml file is
def make_element_with_children(
    name: str, attributes: dict[str, str], children: list[ElementTree.Element] = None
) -> ElementTree.Element:
    if children is None:
        children = []

    element = ElementTree.Element(name, attributes)
    for child in children:
        element.append(child)
    return element
