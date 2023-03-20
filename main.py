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

    def make_board_selector_xml(self, index: int):
        return make_element_with_children(
            "Button",
            {
                "id": self.name,
                "onClick": "makeMap",
                "onMouseEnter": self.author,
                "onMouseExit": "clearInfo",
                "position": get_map_button_position(index),
                "width": "40",
                "height": "20",
                "fontSize": "8",
                "color": self.color,
            },
        )


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
def make_next_map_button(current_page_index: int):
    current_page_number = current_page_index + 1
    return make_element_with_children(
        "Button",
        {
            "onclick": f"maps{current_page_number + 1}",
            "position": MAP_BUTTON_POSITIONS[-1],
            "width": "40",
            "height": "20",
            "fontSize": "8",
            "icon": "More Button",
            "color": "#f3ecd1",
        },
    )


def make_previous_map_button(current_page_index: int):
    current_page_number = current_page_index + 1
    return make_element_with_children(
        "Button",
        {
            "onclick": f"maps{current_page_number - 1}",
            "position": MAP_BUTTON_POSITIONS[4],
            "width": "40",
            "height": "20",
            "fontSize": "8",
            "icon": "Back Button",
            "color": "#f3ecd1",
        },
    )


def generate_maps_xml(maps: list[Map]):
    pages = make_map_pages(maps)

    xml = [
        make_element_with_children(
            "ToggleGroup",
            {"id": f"fanMapButtons{i+1}", "active": "False"},
            page,
        )
        for i, page in enumerate(pages)
    ]

    return xml


def make_map_pages(maps: list[Map]) -> list[list[ElementTree.Element]]:
    remaining_maps = maps.copy()
    pages = []

    current_page_index = 0

    while True:
        # new page
        num_items_on_page = 8
        is_page_before = current_page_index > 0
        if is_page_before:
            num_items_on_page -= 1

        is_page_after = len(remaining_maps) > num_items_on_page
        if is_page_after:
            num_items_on_page -= 1

        items_on_page = remaining_maps[:num_items_on_page]
        remaining_maps = remaining_maps[num_items_on_page:]

        if is_page_before:
            items_on_page.insert(4, make_previous_map_button(current_page_index))
        if is_page_after:
            items_on_page.append(make_next_map_button(current_page_index))

        page = []
        for index, item in enumerate(items_on_page):
            if isinstance(item, Map):
                page.append(item.make_board_selector_xml(index))
            else:
                page.append(item)
        pages.append(page)

        current_page_index += 1
        if not remaining_maps:
            break

    return pages
