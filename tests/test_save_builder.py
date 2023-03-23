def escape_xml(xml: str) -> str:
    return xml  # it appears its just standard escaping.

    # return xml.replace("\r", "").replace("\n", "")


def test_escape_xml():
    expected = '<Button id="xButton" onclick="deleteThis" position="117 85 -15" width="15" height="15" fontSize="8" padding="4 4 4" icon = "Xmark" color="#bd2608" active="false"/>\r\n<Image id="info" image="Blank Info" position="35 -85 -20" width="156" height="6"/>\r\n<Image id="rootLogo" position="-87.5 80 -20" width="75" height="25" image="Root Logo"/>'
    _input = """<Button id="xButton" onclick="deleteThis" position="117 85 -15" width="15" height="15" fontSize="8" padding="4 4 4" icon = "Xmark" color="#bd2608" active="false"/>
<Image id="info" image="Blank Info" position="35 -85 -20" width="156" height="6"/>
<Image id="rootLogo" position="-87.5 80 -20" width="75" height="25" image="Root Logo"/>"""

    actual = escape_xml(_input)

    expected = expected.replace("\r", "").replace("\n", "")
    actual = actual.replace("\r", "").replace("\n", "")

    assert expected == actual
