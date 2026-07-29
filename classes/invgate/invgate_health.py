class InvgateHealth:
    def __init__(self, computer: int, updated_at: str = None, health_rule: str = None, status: str = None):
        self.computer: int = computer
        self.updated_at: str = updated_at
        self.health_rule: str = health_rule
        self.status: str = status

    def to_string(self) -> str:
        string = f"Computer: {self.computer}\n"
        string += f"Updated At: {self.updated_at}\n"
        string += f"Health Rule: {self.health_rule}\n"
        string += f"Status: {self.status}\n"