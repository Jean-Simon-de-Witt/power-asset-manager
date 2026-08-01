class InvgateTag:
    """
    A class for storing Invgate Tag objects in memory.
    """
    def __init__(self, id: int, name: str, color: str = None, description: str = None, smart_tag: bool = False, locked: bool = False):
        """
        Creates a new InvgateTag object.
        
        Arguments:
            id* (int): The unique identifier for each tag object.
            name* (str): The tag's name.
            color (str): The tag's color.
            description (str): The tag's description.
            smart_tag (bool): Whether or not the tag is a smart tag.
            locked (bool): Whether or not the tag is locked.

        Returns:
            None:
        """
        self.id: int = id
        self.name: str = name
        self.color: str = color
        self.description: str = description
        self.smart_tag: bool = smart_tag
        self.locked: bool = locked

    def to_string(self) -> str:
        """
        Exports the objet's properties as a formatted string.
        
        Arguments:
            None:

        Returns:
            string (str): The object's properties as a formatted string.
        """
        string = f"ID: {self.id}\n"
        string += f"Name: {self.name}\n"
        string += f"Color: {self.color}\n"
        string += f"Description: {self.description}\n"
        string += f"Smart Tag: {self.smart_tag}\n"
        string += f"Locked: {self.locked}\n"
        return string
