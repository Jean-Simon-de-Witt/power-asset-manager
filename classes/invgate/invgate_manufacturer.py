from classes.invgate.invgate_object import InvgateObject
class InvgateManufacturer(InvgateObject):
    """
    A class for storing Invgate Manufacturer objects in memory.
    """
    def __init__(self, id: int, name: str):
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