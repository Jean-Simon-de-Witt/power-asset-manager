from classes.invgate.invgate_object import InvgateObject

class InvgateStatus(InvgateObject):
    """
    A class for storing Invgate Status objects in memory. Inherits from the InvgateObject class.
    """
    def __init__(self, id: int, name: str, description: str, behavior: str, is_default: bool):
        """Creates a new InvgateStatus object.

        Args:
            id (int): The status' ID.
            name (str): The status' name.
            description (str): The status' description.
            behavior (str): The status' behavior.
            is_default (bool): Whether or not the status is default.
        """

        self.id: int = id
        self.name: str = name
        self.description: str = description
        self.behavior: str = behavior
        self.is_default: bool = is_default