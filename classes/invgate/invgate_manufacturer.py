class InvgateManufacturer:
    def __init__(self, id: int, name: str):
        self.id: int = id
        self.name: str = name

    def to_string(self) -> str:
        string = f"ID: {self.id}\n"
        string += f"Name: {self.name}\n"
        return string