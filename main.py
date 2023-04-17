from pathlib import Path

from fan_maps import REAL_MAPS
from save_builder import build_xml, build_save, save_to_tts

template = Path("data/xml_template.xml").read_text()


def build():
    xml = build_xml(REAL_MAPS)
    full_save = build_save(xml)
    Path("data/generated_out.json").write_text(full_save)
    save_to_tts(full_save)
    print("done")


if __name__ == "__main__":
    build()
