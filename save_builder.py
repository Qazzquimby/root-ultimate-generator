import json
from pathlib import Path
import jinja2 as jinja2

from fan_maps import Map, get_map_elements
from xml_utilities import to_string

xml_template_path = Path("data/xml_template.xml")


def build_xml(maps: list[Map]) -> str:
    maps_elements = get_map_elements(maps)
    element_xmls = [to_string(page_element) for page_element in maps_elements]
    xml = "\n".join(element_xmls)
    template = xml_template_path.read_text()
    full_xml = jinja2.Template(template).render(fanMapButtons=xml)
    return full_xml


def build_save(xml: str) -> str:
    xml = json.dumps(xml)
    # drop " from start and end
    xml = xml[1:-1]

    lua = Path("data/real_lua_script.txt").read_text()

    save_template_path = Path("data/save_template.json")
    save_template = save_template_path.read_text()
    # faction_board_lua_script
    # faction_board_xml
    full_save = jinja2.Template(save_template).render(
        faction_board_lua_script=lua,
        faction_board_xml=xml,
    )
    return full_save
