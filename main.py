from pathlib import Path

from fan_maps import get_map_elements, REAL_MAPS
from save_builder import build_xml, build_save

template = Path("data/xml_template.xml").read_text()


def build():
    xml = build_xml(REAL_MAPS)
    full_save = build_save(xml)
    Path("data/generated_out.json").write_text(full_save)
    save_to_tts(full_save)
    print("done")


def save_to_tts(save: str):
    tts_save_path = Path(
        r"C:\Users\User\Documents\my games\Tabletop Simulator\Saves/root_generation.json"
    )
    tts_save_path.write_text(save)


if __name__ == "__main__":
    build()
