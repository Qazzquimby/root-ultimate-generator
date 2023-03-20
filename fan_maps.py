# <ToggleGroup id="fanMapButtons1" active="False">
#     <Button id="Summer Map" onClick="makeMap" onMouseEnter = "infoNevakanezahAndSlug" onMouseExit="clearInfo" position="-25 5 -20" width="40" height="20" fontSize="8" icon ="Summer Map" color="#4b4d35"/>
#     <Button id="Legends Map" onClick="makeMap" onMouseEnter = "infoSlug" onMouseExit="clearInfo" position="15 5 -20" width="40" height="20" fontSize="8" icon ="Legends Map" color="#FAE5B3"/>
#     <Button id="Urban Map" onClick="makeMap" onMouseEnter = "infoSlug" onMouseExit="clearInfo" position="55 5 -20" width="40" height="20" fontSize="8" icon ="Urban Map" color="#9b8551"/>
#     <Button id="Lost Woodland Map" onclick="makeMap" onMouseEnter = "infoEndgamer" onMouseExit="clearInfo" position="95 5 -20" width="40" height="20" fontSize="8" icon ="Lost Woodland Map" color="#5b5a36"/>
#
#     <Button id="Gorge Map" onClick="makeMap" onMouseEnter = "infoLordOfTheBoard" onMouseExit="clearInfo" position="-25 -15 -20" width="40" height="20" fontSize="8" icon ="Gorge Map" color="#61746b"/>
#     <Button id="Treasure Island Map" onclick="makeMap" position="15 -15 -20" width="40" height="20" onMouseEnter = "infoSupacatone" onMouseExit="clearInfo" fontSize="8" icon ="Treasure Island Map" color="#567826"/>
#     <Button id="The Deep Woods Map" onclick="makeMap" onMouseEnter="infoSlug" onMouseExit="clearInfo" position="55 -15 -20" width="40" height="20" fontSize="8" icon ="Deep Woods Map" color="#3f4839"/>
#     <Button onclick="maps2" position="95 -15 -20" width="40" height="20" fontSize="8" icon ="More Button" color="#f3ecd1"/>
# </ToggleGroup>
#
#
#
# <ToggleGroup id="fanMapButtons2" active="False">
#   <Button id="Australia Map" onclick="makeMap" onMouseEnter = "infoVatechman3" onMouseExit="clearInfo" position="-25 5 -20" width="40" height="20" fontSize="8" icon ="Australia Map" color="#899c58"/>
#   <Button id="Narrows and Islets Map" onclick="makeMap" onMouseEnter = "infoHierotitanAndLeonatus" onMouseExit="clearInfo" position="15 5 -20" width="40" height="20" fontSize="8" icon ="Narrows and Islets Map" color="#9c9a7b"/>
#   <Button id="Tunnel Unraveled Map" onclick="makeMap" onMouseEnter = "infoTunnelMap" onMouseExit="clearInfo" position="55 5 -20" width="40" height="20" fontSize="8" icon ="Tunnel Unraveled Map" color="#422e19"/>
#   <Button id="Tropics Map" onclick="makeMap" onMouseEnter = "infoJ444" onMouseExit="clearInfo" position="95 5 -20" width="40" height="20" fontSize="8" icon ="Tropics Map" color="#7e986c"/>
#   <Button id="The Wastelands Map" onclick="makeMap" onMouseEnter = "infoSlug" onMouseExit="clearInfo" position="15 -15 -20" width="40" height="20" fontSize="8" icon ="Wastelands Map" color="#83805b"/>
#
#
#   <Button onclick="maps1" position="-25 -15 -20" width="40" height="20" fontSize="8" icon ="Back Button" color="#f3ecd1"/>
# </ToggleGroup>
from xml.etree import ElementTree as ElementTree

import pydantic

from xml_utilities import make_element_with_children


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
