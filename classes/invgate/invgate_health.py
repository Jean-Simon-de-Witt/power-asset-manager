from classes.invgate.invgate_object import InvgateObject

class InvgateHealth(InvgateObject):
    """
    A class for storing Invgate Health object in memory. Inherits from the InvgateObject class.
    """
    def __init__(self, computer: int, updated_at: str, health_rule: str, status: str):
        """Creates a new InvgateHealth object.

        Args:
            computer (int): The computer's ID.
            updated_at (str): When last the health was updated.
            health_rule (str): The health rule.
            status (str): The computer's health status.
        """

        self.computer: int = computer
        self.updated_at: str = updated_at
        self.health_rule: str = health_rule
        self.status: str = status