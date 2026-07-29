class InvgateStatus:
    def __init__(self, id, name, description = None, behavior = None, is_default = False):
        self.id = id
        self.name = name
        self.description = description
        self.behavior = behavior
        self.is_default = is_default

    def to_string(self):
        string = f"ID: {self.id}\n"
        string += f"Name: {self.name}\n"
        string += f"Description: {self.description}\n"
        string += f"Behavior: {self.behavior}\n"
        string += f"Is Default: {self.is_default}\n"
        return string