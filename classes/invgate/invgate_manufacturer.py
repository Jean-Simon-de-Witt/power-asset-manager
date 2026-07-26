class InvgateManufacturer:
    def __init__(self, id = None, name = None):
        self.id = id
        self.name = name

    def to_string(self) -> str:
        if self.id and self.name:
            string = f"ID: {self.id}\nName: {self.name}\n"
        else:
            string = "Manufacturer not found."
        return string