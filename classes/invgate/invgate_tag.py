class InvgateTag:
    def __init__(self, id: int, name: str, color: str = None, description: str = None, smart_tag: bool = False, locked: bool = False):
        self.id: int = id
        self.name: str = name
        self.color: str = color
        self.description: str = description
        self.smart_tag: bool = smart_tag
        self.locked: bool = locked

    def to_string(self) -> str:
        string = f"ID: {self.id}\n"
        string += f"Name: {self.name}\n"
        string += f"Color: {self.color}\n"
        string += f"Description: {self.description}\n"
        string += f"Smart Tag: {self.smart_tag}\n"
        string += f"Locked: {self.locked}\n"
        return string
