class InvgateHealth:
    """
    A class for storing Invgate Health object in memory.
    """
    def __init__(self, computer: int, updated_at: str, health_rule: str, status: str):
        """
        Creates a new InvgateHealth object.
        
        Arguments:
            computer* (int): The unique identifier linking to the asset's ID.
            updated_at (str): The time indicating when last the asset's health status was updated.
            health_rule (str): The asset's health rule.
            status (str): The asset's health status.

        Returns:
            None:
        """
        self.computer: int = computer
        self.updated_at: str = updated_at
        self.health_rule: str = health_rule
        self.status: str = status

    def to_string(self) -> str:
        """
        Exports the object's properties as a formatted string.

        Arguments:
            None:
        
        Returns:
            string (str): The object's properties as a formatted string.
        """
        string = f"Computer: {self.computer}\n"
        string += f"Updated At: {self.updated_at}\n"
        string += f"Health Rule: {self.health_rule}\n"
        string += f"Status: {self.status}\n"