from classes.invgate.invgate_object import InvgateObject

class InvgateTag(InvgateObject):
    """
    A class for storing Invgate Tag objects in memory.
    """
    def __init__(self, id: int, name: str, color: str, description: str, smart_tag: bool, locked: bool):

        self.id: int = id
        self.name: str = name
        self.color: str = color
        self.description: str = description
        self.smart_tag: bool = smart_tag
        self.locked: bool = locked