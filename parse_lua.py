import dataclasses

from luaparser import ast


def find_assignment(lua_tree, target):
    for node in ast.walk(lua_tree):
        if isinstance(node, ast.Assign):
            if isinstance(node.targets[0], ast.Name) and node.targets[0].id == target:
                fields = node.values[0].fields
                if fields:
                    assignments = [ast.to_lua_source(field.value) for field in fields]
                    dicts = []
                    for assignment in assignments:
                        dict_ = {}
                        for split in assignment.split(","):
                            try:
                                key, value = split.split("=", 1)
                                key = (
                                    key.replace("{", "")
                                    .replace("}", "")
                                    .replace('"', "")
                                    .replace("'", "")
                                    .strip()
                                )
                                value = (
                                    value.replace("{", "")
                                    .replace("}", "")
                                    .replace('"', "")
                                    .replace("'", "")
                                    .strip()
                                )
                                dict_[key] = value
                            except (IndexError, ValueError):
                                continue
                        dicts.append(dict_)
                    return dicts


@dataclasses.dataclass
class FanFaction:
    name: str
    lua: str
    icon: str
    image: str
    adset_card_face: str


def get_everything(lua):
    everything = {}
    _, everything_defintion_lua, other_lua = lua.split("----#include Shard/everything")
    everything_splits = everything_defintion_lua.split("EVERYTHING['")
    for everything_split in everything_splits:
        # eg 'Standard']['Harrier'] = {...'
        try:
            category, rest = everything_split.split("']['", 1)
            name, content = rest.split("'] = ", 1)
        except (IndexError, ValueError):
            continue
        everything.setdefault(category, {})[name] = content
    return everything, other_lua


def get_assets(lua):
    lua_tree = ast.parse(lua.replace("!=", "~="))
    assets_ = find_assignment(lua_tree, "assets")
    assets = {asset["name"]: asset["url"] for asset in assets_}
    # {        name = "Spinners of Mercy Icon", url = "http://cloud-3.steamusercontent.com/ugc/1920249469919849760/D2CF1773DD8589DCD09911AF0EA349324847B62F/"},
    # {name = "Spinners of Mercy",url = "http://cloud-3.steamusercontent.com/ugc/1728793291754416260/AE57D54645432C8981422F9051666710651D0A7B/"},
    return assets


def get_adset_draft_faces(lua):
    # _G["WWAdsetCardFaces"]["Spinners of Mercy"] = "http://cloud-3.steamusercontent.com/ugc/1867301389180149376/CA21C6BD3BD6BDDFC59E2FAB811A40EB16BC36F2/"
    g_adset_draft_faces = {}
    for split in lua.split('_G["WWAdsetCardFaces"]["')[1:]:
        try:
            name, rest = split.split('"] = "', 1)
            url, _ = rest.split('"', 1)
        except (IndexError, ValueError):
            continue
        g_adset_draft_faces[name] = url
    return g_adset_draft_faces


def _get_fan_factions(everything, assets, adset_draft_faces):
    factions = []
    for name, lua in everything["Fan Factions"].items():
        image = assets.get(name, None)

        icon = assets.get(name + " Icon", None)
        if not icon:
            assets.get(name + "Icon", None)

        adset_card_face = adset_draft_faces.get(name, None)

        if not image and not icon and not adset_card_face:
            continue

        faction = FanFaction(
            name=name,
            lua=lua,
            icon=icon,
            image=image,
            adset_card_face=adset_card_face,
        )
        factions.append(faction)


def get_fan_factions():
    lua_file = open("data/real_lua_script.lua", "r")
    lua = lua_file.read()

    everything, other_lua = get_everything(lua)
    assets = get_assets(other_lua)
    adset_draft_faces = get_adset_draft_faces(other_lua)

    factions = _get_fan_factions(everything, assets, adset_draft_faces)

    return factions


if __name__ == "__main__":
    get_fan_factions()
