from pathlib import Path
import xml.etree.ElementTree as ElementTree
import pydantic

template = Path("xml_template.xml").read_text()


def generate_faction_selector():
    return template  # todo


class Map(pydantic.BaseModel):
    name: str
    author: str
    color: str


def generate_maps_xml(maps: list[Map]):
    xml = ElementTree.Element(
        "ToggleGroup", {"id": "fanMapButtons1", "active": "False"}
    )
    xml.append(
        ElementTree.Element(
            "Test Map 1", {"author": "Test Author 1", "color": "#000001"}
        )
    )
    return xml


# jinja template is named for an xml file is
