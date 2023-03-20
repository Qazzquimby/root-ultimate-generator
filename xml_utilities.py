from xml.etree import ElementTree as ElementTree


def make_element_with_children(
    name: str, attributes: dict[str, str], children: list[ElementTree.Element] = None
) -> ElementTree.Element:
    if children is None:
        children = []

    element = ElementTree.Element(name, attributes)
    for child in children:
        element.append(child)
    return element
