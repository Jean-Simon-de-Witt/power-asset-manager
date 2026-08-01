class InvgateStatus:
    """
    A class for storing Invgate Status objects in memory.
    """
    def __init__(self, id: int, name: str, description: str = None, behavior: str = None, is_default: bool = False):
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

    def to_string(self):
        """
        Exports the object's properties as a formatted string.
        
        Arguments:
            None:

        Returns:
            string (str): The object's properties as a formatted string.
        """
        string = f"ID: {self.id}\n"
        string += f"Name: {self.name}\n"
        string += f"Description: {self.description}\n"
        string += f"Behavior: {self.behavior}\n"
        string += f"Is Default: {self.is_default}\n"
        return string