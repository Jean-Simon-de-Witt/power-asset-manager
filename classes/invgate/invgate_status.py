class InvgateStatus:
    def __init__(self, id, name, full_path = None, description = None):
        self.id = id
        self.name = name
        self.full_path = full_path
        self.description = description

    def to_string(self):
        return f"ID: {self.id}\nName: {self.name}\nFull Path: {self.full_path}\nDescription: {self.description}\n"