from classes.invgate.invgate_object import InvgateObject
class InvgateManufacturer(InvgateObject):
    """
    A class for storing Invgate Manufacturer objects in memory. Inherits from the InvgateObject class.
    """
    def __init__(self, id: int, name: str):
        """Creates a new InvgateManufacturer object.

        Args:
            id (int): The manufacturer's ID.
            name (str): The manufacturer's name.
        """
        self.id: int = id
        self.name: str = name