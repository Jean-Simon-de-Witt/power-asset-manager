from classes.invgate.invgate_object import InvgateObject

class InvgateTag(InvgateObject):
    """
    A class for storing InvgateTag objects in memory. Inherits from the InvgateObject class.
    """
    def __init__(self, id: int, name: str, color: str, description: str, smart_tag: bool, locked: bool):
        """Creates a new InvgateTag object.

        Args:
            id (int): The tag's ID.
            name (str): The tag's name.
            color (str): The tag's color.
            description (str): The tag's description.
            smart_tag (bool): Whether or not the tag is a smart tag.
            locked (bool): Whether or not the tag is locked.
        """

        self.id: int = id
        self.name: str = name
        self.color: str = color
        self.description: str = description
        self.smart_tag: bool = smart_tag
        self.locked: bool = locked