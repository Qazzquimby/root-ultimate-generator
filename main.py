from pathlib import Path

template = Path("xml_template.xml").read_text()

def generate_faction_selector():
    return template


# jinja template is named for an xml file is