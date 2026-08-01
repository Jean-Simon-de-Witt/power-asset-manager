class InvgateManufacturer:
    """
    A class for storing Invgate Manufacturer objects in memory.
    """
    def __init__(self, name: str, id: int = None):
        """
        Creates a new InvgateManufacturer object.
        
        Arguments:
            name* (str): The manufacturer's name.
            id (int): The unique identifier for each manufacturer object.

        Returns:
            None:
        """
        self.id: int = id
        self.name: str = name

    def to_string(self) -> str:
        """
        Exports the object's properties as a formatted string.
        
        Arguments:
            None:

        Returns:
            string (str): The object's properties as a formatted string.
        """
        string = f"ID: {self.id}\n"
        string += f"Name: {self.name}\n"
        return string