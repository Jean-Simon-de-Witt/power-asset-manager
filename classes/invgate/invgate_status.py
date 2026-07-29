class InvgateStatus:
    def __init__(self, id: int, name: str, description: str = None, behavior: str = None, is_default: bool = False):
        self.id: int = id
        self.name: str = name
        self.description: str = description
        self.behavior: str = behavior
        self.is_default: str = is_default

    def to_string(self):
        string = f"ID: {self.id}\n"
        string += f"Name: {self.name}\n"
        string += f"Description: {self.description}\n"
        string += f"Behavior: {self.behavior}\n"
        string += f"Is Default: {self.is_default}\n"
        return string