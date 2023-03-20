from xml.etree import ElementTree as ElementTree

import pydantic

from xml_utilities import make_element_with_children

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

BUTTON_PROPERTIES = {
    "width": "40",
    "height": "20",
    "fontSize": "8",
}


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
                "color": self.color,
                **BUTTON_PROPERTIES,
            },
        )


def get_map_button_position(index: int):
    return MAP_BUTTON_POSITIONS[index % len(MAP_BUTTON_POSITIONS)]


def make_next_map_button(current_page_index: int):
    current_page_number = current_page_index + 1
    return make_element_with_children(
        "Button",
        {
            "onclick": f"maps{current_page_number + 1}",
            "position": MAP_BUTTON_POSITIONS[-1],
            "icon": "More Button",
            "color": "#f3ecd1",
            **BUTTON_PROPERTIES,
        },
    )


def make_previous_map_button(current_page_index: int):
    current_page_number = current_page_index + 1
    return make_element_with_children(
        "Button",
        {
            "onclick": f"maps{current_page_number - 1}",
            "position": MAP_BUTTON_POSITIONS[4],
            "icon": "Back Button",
            "color": "#f3ecd1",
            **BUTTON_PROPERTIES,
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


maps = [
    Map(name="Summer Map", author="infoNevakanezahAndSlug", color="#4b4d35"),
    Map(name="Legends Map", author="infoSlug", color="#FAE5B3"),
    Map(name="Urban Map", author="infoSlug", color="#9b8551"),
    Map(name="Lost Woodland Map", author="infoEndgamer", color="#5b5a36"),
    Map(name="Gorge Map", author="infoLordOfTheBoard", color="#61746b"),
    Map(name="Treasure Island Map", author="infoSupacatone", color="#567826"),
    Map(name="The Deep Woods Map", author="infoSlug", color="#3f4839"),
    Map(name="Australia Map", author="infoVatechman3", color="#899c58"),
    Map(
        name="Narrows and Islets Map",
        author="infoHierotitanAndLeonatus",
        color="#9c9a7b",
    ),
    Map(name="Tunnel Unraveled Map", author="infoTunnelMap", color="#422e19"),
    Map(name="Tropics Map", author="infoJ444", color="#7e986c"),
    Map(name="The Wastelands Map", author="infoSlug", color="#83805b"),
]
