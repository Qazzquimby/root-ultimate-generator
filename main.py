from pathlib import Path

template = Path("xml_template.xml").read_text()


def generate_faction_selector():
    return template  # todo

# <Button onclick="maps2" position="95 -15 -20" width="40" height="20" fontSize="8" icon ="More Button" color="#f3ecd1"/>


