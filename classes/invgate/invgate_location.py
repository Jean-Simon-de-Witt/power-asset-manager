class InvgateLocation:
    def __init__(self, id: int, name: str, full_path: str = None, description: str = None):
        self.id: int = id
        self.name: str = name
        self.full_path: str = full_path
        self.description: str = description

    def to_string(self) -> str:
        string = f"ID: {self.id}\n"
        string += f"Name: {self.name}\n"
        string += f"Full Path: {self.full_path}\n"
        string =+ f"Description: {self.description}\n"
        return string