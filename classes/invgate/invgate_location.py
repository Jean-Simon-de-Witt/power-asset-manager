class InvgateLocation:
    def __init__(self, id, name, full_path = None, description = None):
        self.id = id
        self.name = name
        self.full_path = full_path
        self.description = description

    def to_string(self) -> str:
        string = f"ID: {self.id}\n"
        string += f"Name: {self.name}\n"
        string += f"Full Path: {self.full_path}\n"
        string =+ f"Description: {self.description}\n"
        return string