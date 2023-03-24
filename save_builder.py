from pathlib import Path
from xml.etree import ElementTree
import jinja2 as jinja2

from fan_maps import Map, generate_maps_xml
from xml_utilities import to_string

xml_template_path = Path("xml_template.xml")


def build_xml(fan_maps: list[Map]) -> str:
    xml = "\n".join([to_string(page) for page in generate_maps_xml(fan_maps)])
    # use jinja template
    template = xml_template_path.read_text()
    full_xml = jinja2.Template(template).render(fanMapButtons=xml)
    return full_xml
