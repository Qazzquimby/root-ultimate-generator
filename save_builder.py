import json
from pathlib import Path
import jinja2 as jinja2

from fan_maps import Map, get_map_elements
from parse_lua import FanFaction
from xml_utilities import to_string

xml_template_path = Path("data/xml_template.xml")


def build_xml(maps: list[Map]) -> str:
    maps_elements = get_map_elements(maps)
    element_xmls = [to_string(page_element) for page_element in maps_elements]
    xml = "\n".join(element_xmls)
    template = xml_template_path.read_text()
    full_xml = jinja2.Template(template).render(fanMapButtons=xml)
    return full_xml


def make_fan_factions_everything_string(fan_factions: list[FanFaction]) -> str:
    fan_factions_everything = []
    for fan_faction in fan_factions:
        everything_string = (
            f'Everything["Fan Factions"]["{fan_faction.name}"] = {fan_faction.lua}'
        )
        fan_factions_everything.append(everything_string)
    fan_factions_everything_string = "\n".join(fan_factions_everything)
    return fan_factions_everything_string


def build_lua(fan_factions: list[FanFaction]) -> str:
    fan_factions_everything_string = make_fan_factions_everything_string(fan_factions)

    # Todo still need to add the assets for image, icon, etc

    lua_template = Path("data/lua_script_template.lua").read_text()
    # lua = jinja2.Template(lua_template).render(fan_factions_everything=fan_factions_everything_string)
    target = "{{fan_factions_everything}}"
    lua = lua_template.replace(target, fan_factions_everything_string)
    return lua


def build_save_from_lua_and_xml(lua: str, xml: str) -> str:
    xml = json.dumps(xml)[1:-1]
    # drop " from start and end

    return Path("data/save.json").read_text()  # todo remove

    save_template_path = Path("data/save_template.json")
    save_template = save_template_path.read_text()
    # faction_board_lua_script
    # faction_board_xml

    escaped_lua = json.dumps(lua)[1:-1]

    full_save = jinja2.Template(save_template).render(
        faction_board_lua_script=escaped_lua,
        faction_board_xml=xml,
    )
    return full_save


def build_save() -> str:
    xml = build_xml([])
    lua = build_lua(
        [
            FanFaction(
                name="test",
                lua='{color=\'\', data={\r\n{move_to={ 17.820294, 0.100003, 7.001048 }, json=[[{"GUID": "2802e3","Name": "Custom_Tile","Transform": {"posX": 109.833481,"posY": 35.6900864,"posZ": -44.0897942,"rotX": 0.0175815262,"rotY": 180.033173,"rotZ": 0.0801393241,"scaleX": 0.6283841,"scaleY": 1.0,"scaleZ": 0.6283841},"Nickname": "Berserker VP","Description": "","GMNotes": "","ColorDiffuse": {"r": 0.2491281,"g": 0.1618897,"b": 0.103730746},"LayoutGroupSortIndex": 0,"Value": 0,"Locked": false,"Grid": true,"Snap": true,"IgnoreFoW": false,"MeasureMovement": false,"DragSelectable": true,"Autoraise": true,"Sticky": false,"Tooltip": true,"GridProjection": false,"HideWhenFaceDown": false,"Hands": false,"CustomImage": {"ImageURL": "http://cloud-3.steamusercontent.com/ugc/1756947110727727846/25BC7EEE0A12526D589C70EDD0B20F02B4D9BAB0/","ImageSecondaryURL": "","ImageScalar": 1.0,"WidthScale": 0.0,"CustomTile": {"Type": 3,"Thickness": 0.149999857,"Stackable": false,"Stretch": true}},"LuaScript": "","LuaScriptState": "","XmlUI": ""\r\n}]]},{move_to={ 3.929355, 0.200024, -7.67924 }, json=[[{"GUID": "b8cc62","Name": "Custom_Tile","Transform": {"posX": 95.944725,"posY": 35.7049866,"posZ": -58.77214,"rotX": 0.01759547,"rotY": 180.024338,"rotZ": 0.08013402,"scaleX": 0.6283841,"scaleY": 1.0,"scaleZ": 0.6283841},"Nickname": "","Description": "","GMNotes": "","ColorDiffuse": {"r": 0.0,"g": 0.0,"b": 0.0},"LayoutGroupSortIndex": 0,"Value": 0,"Locked": false,"Grid": true,"Snap": true,"IgnoreFoW": false,"MeasureMovement": false,"DragSelectable": true,"Autoraise": true,"Sticky": false,"Tooltip": true,"GridProjection": false,"HideWhenFaceDown": false,"Hands": false,"CustomImage": {"ImageURL": "http://cloud-3.steamusercontent.com/ugc/1807607729518280734/21969C2E34BD63C9BE519E77D6F1AB921D9D8802/","ImageSecondaryURL": "http://cloud-3.steamusercontent.com/ugc/1807607729518281205/9CF0A55A6A7A369DD069D5C3425CC99B04480D78/","ImageScalar": 1.0,"WidthScale": 0.0,"CustomTile": {"Type": 3,"Thickness": 0.1,"Stackable": false,"Stretch": true}},"LuaScript": "","LuaScriptState": "","XmlUI": ""\r\n}]]},{move_to={ 2.411863, 0.200024, -7.708361 }, json=[[{"GUID": "a3c421","Name": "Custom_Tile","Transform": {"posX": 94.42724,"posY": 35.7071,"posZ": -58.801487,"rotX": 0.01759522,"rotY": 180.024445,"rotZ": 0.0801340938,"scaleX": 0.6283841,"scaleY": 1.0,"scaleZ": 0.6283841},"Nickname": "","Description": "","GMNotes": "","ColorDiffuse": {"r": 0.0,"g": 0.0,"b": 0.0},"LayoutGroupSortIndex": 0,"Value": 0,"Locked": false,"Grid": true,"Snap": true,"IgnoreFoW": false,"MeasureMovement": false,"DragSelectable": true,"Autoraise": true,"Sticky": false,"Tooltip": true,"GridProjection": false,"HideWhenFaceDown": false,"Hands": false,"CustomImage": {"ImageURL": "http://cloud-3.steamusercontent.com/ugc/1807607729518280734/21969C2E34BD63C9BE519E77D6F1AB921D9D8802/","ImageSecondaryURL": "http://cloud-3.steamusercontent.com/ugc/1807607729518281205/9CF0A55A6A7A369DD069D5C3425CC99B04480D78/","ImageScalar": 1.0,"WidthScale": 0.0,"CustomTile": {"Type": 3,"Thickness": 0.1,"Stackable": false,"Stretch": true}},"LuaScript": "","LuaScriptState": "","XmlUI": ""\r\n}]]},{move_to={ 0.939181, 0.200024, -7.661135 }, json=[[{"GUID": "7ed3bb","Name": "Custom_Tile","Transform": {"posX": 92.95455,"posY": 35.7091751,"posZ": -58.75448,"rotX": 0.017591795,"rotY": 180.026962,"rotZ": 0.0801349,"scaleX": 0.6283841,"scaleY": 1.0,"scaleZ": 0.6283841},"Nickname": "","Description": "","GMNotes": "","ColorDiffuse": {"r": 0.0,"g": 0.0,"b": 0.0},"LayoutGroupSortIndex": 0,"Value": 0,"Locked": false,"Grid": true,"Snap": true,"IgnoreFoW": false,"MeasureMovement": false,"DragSelectable": true,"Autoraise": true,"Sticky": false,"Tooltip": true,"GridProjection": false,"HideWhenFaceDown": false,"Hands": false,"CustomImage": {"ImageURL": "http://cloud-3.steamusercontent.com/ugc/1807607729518285785/DAFA6554DCB3AD0B6E37419A3E649DDE6AFB6358/","ImageSecondaryURL": "http://cloud-3.steamusercontent.com/ugc/1807607729518286301/4A1B9AE0AB6FD7F6E1B7BF6C7212A88B15E2C27D/","ImageScalar": 1.0,"WidthScale": 0.0,"CustomTile": {"Type": 3,"Thickness": 0.1,"Stackable": false,"Stretch": true}},"LuaScript": "","LuaScriptState": "","XmlUI": ""\r\n}]]},{move_to={ -4.300522, 0.200024, -1.350021 }, json=[[{"GUID": "7909c8","Name": "Custom_Tile","Transform": {"posX": 87.71392,"posY": 35.71845,"posZ": -52.44414,"rotX": 0.017580511,"rotY": 180.034943,"rotZ": 0.0801371858,"scaleX": 0.6283841,"scaleY": 1.0,"scaleZ": 0.6283841},"Nickname": "","Description": "","GMNotes": "","ColorDiffuse": {"r": 0.0,"g": 0.0,"b": 0.0},"LayoutGroupSortIndex": 0,"Value": 0,"Locked": false,"Grid": true,"Snap": true,"IgnoreFoW": false,"MeasureMovement": false,"DragSelectable": true,"Autoraise": true,"Sticky": false,"Tooltip": true,"GridProjection": false,"HideWhenFaceDown": false,"Hands": false,"CustomImage": {"ImageURL": "http://cloud-3.steamusercontent.com/ugc/1807607729518312040/02A17E7AC9961890D9D21726D6F0F7B09934BF8C/","ImageSecondaryURL": "http://cloud-3.steamusercontent.com/ugc/1807607729518312473/3C83F72969B2FB573E306167E1CDBFCD0E2D2DD1/","ImageScalar": 1.0,"WidthScale": 0.0,"CustomTile": {"Type": 3,"Thickness": 0.1,"Stackable": false,"Stretch": true}},"LuaScript": "","LuaScriptState": "","XmlUI": ""\r\n}]]},{move_to={ -4.84138, 0.099999, 5.141591 }, json=[[{"GUID": "771178","Name": "Custom_Model","Transform": {"posX": 87.1721039,"posY": 35.7212,"posZ": -45.95261,"rotX": 0.01765477,"rotY": 180.0008,"rotZ": 0.08022244,"scaleX": 0.3531452,"scaleY": 0.353144079,"scaleZ": 0.5201159},"Nickname": "Berserker VB","Description": "","GMNotes": "","ColorDiffuse": {"r": 1.0,"g": 1.0,"b": 1.0},"LayoutGroupSortIndex": 0,"Value": 0,"Locked": false,"Grid": true,"Snap": false,"IgnoreFoW": false,"MeasureMovement": false,"DragSelectable": true,"Autoraise": true,"Sticky": false,"Tooltip": true,"GridProjection": false,"HideWhenFaceDown": false,"Hands": false,"CustomMesh": {"MeshURL": "http://cloud-3.steamusercontent.com/ugc/1756947110726844580/3AE35DF70015A15411B5FCDA661698F03B8A6C4C/","DiffuseURL": "http://cloud-3.steamusercontent.com/ugc/1756947110726845177/9A6829276246D9FFC8FEAFBDA7147B52CF80B6BD/","NormalURL": "","ColliderURL": "http://cloud-3.steamusercontent.com/ugc/1756947110726844580/3AE35DF70015A15411B5FCDA661698F03B8A6C4C/","Convex": true,"MaterialIndex": 1,"TypeIndex": 1,"CastShadows": true},"LuaScript": "","LuaScriptState": "","XmlUI": ""\r\n}]]},{move_to={ 9.53063, 0.213693, -9.30927 }, json=[[{"GUID": "dd520a","Name": "CardCustom","Transform": {"posX": 101.546394,"posY": 35.8103447,"posZ": -60.4013748,"rotX": 0.0168966185,"rotY": 180.03038,"rotZ": 0.0797878951,"scaleX": 2.33,"scaleY": 1.0,"scaleZ": 2.33},"Nickname": "","Description": "","GMNotes": "","ColorDiffuse": {"r": 0.713235259,"g": 0.713235259,"b": 0.713235259},"LayoutGroupSortIndex": 0,"Value": 0,"Locked": true,"Grid": true,"Snap": true,"IgnoreFoW": false,"MeasureMovement": false,"DragSelectable": true,"Autoraise": true,"Sticky": false,"Tooltip": true,"GridProjection": false,"HideWhenFaceDown": true,"Hands": true,"CardID": 14300,"SidewaysCard": false,"CustomDeck": {"143": {"FaceURL": "http://cloud-3.steamusercontent.com/ugc/1755820943820932760/09358C3415355BCD25C0B5204E48850ED250A451/","BackURL": "http://cloud-3.steamusercontent.com/ugc/1807607729518329599/8255A8EFCFB2BD474C3F698579FBBE70662F8CEA/","NumWidth": 1,"NumHeight": 1,"BackIsHidden": true,"UniqueBack": false,"Type": 0}},"LuaScript": "","LuaScriptState": "","XmlUI": ""\r\n}]]},}}\r\n\r\n',
                icon="http://cloud-3.steamusercontent.com/ugc/1857179401550092503/A52FA339323BD25DE4B44AA03B861CA2EB6E9A9D/",
                image="",
                adset_card_face="",
            )
        ]
    )
    save = build_save_from_lua_and_xml(lua, xml)
    return save


def save_to_tts(save: str, name: str):
    tts_save_path = Path(
        rf"C:\Users\User\Documents\my games\Tabletop Simulator\Saves/root_generation_{name}.json"
    )
    tts_save_path.write_text(save)


if __name__ == "__main__":
    save = build_save()
    save_to_tts(save, "empty")
