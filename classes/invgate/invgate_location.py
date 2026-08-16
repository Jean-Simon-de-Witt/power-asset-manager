from classes.invgate.invgate_object import InvgateObject
class InvgateLocation(InvgateObject):
    """
    A class for storing Invgate Location objects in memory. Inherits from the InvgateObject class.
    """
    def __init__(self, id: int, name: str, full_path: str, description: str, content_type: str):
        """Creates a new InvgateLocation object.

        Args:
            id (int): The location's ID.
            name (str): The location's name.
            full_path (str): The location's full path.
            description (str): The location's description.
            content_type (str): The location's content type.
        """
        self.id: int = id
        self.name: str = name
        self.full_path: str = full_path
        self.description: str = description
        self.content_type: str = content_type