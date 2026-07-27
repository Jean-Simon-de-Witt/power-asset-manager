class InvgateManufacturer:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_string(self) -> str:
        return f"ID: {self.id}\nName: {self.name}\n"