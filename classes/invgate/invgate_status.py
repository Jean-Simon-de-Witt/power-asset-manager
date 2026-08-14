from classes.invgate.invgate_object import InvgateObject

class InvgateStatus(InvgateObject):
    """
    A class for storing Invgate Status objects in memory.
    """
    def __init__(self, id: int, name: str, description: str, behavior: str, is_default: bool):
        """
        Creates a new InvgateStatus object.
        
        Arguments:
            id* (int): The unique identifier for each status object.
            name* (str): The status' name.
            description (str): The status' description.
            behavior (str): The status' behavior.
            is_default (bool): Whether or not the status is default.

        Returns:
            None:
        """
        self.id: int = id
        self.name: str = name
        self.description: str = description
        self.behavior: str = behavior
        self.is_default: bool = is_default