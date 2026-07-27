class InvgateTag:
    def __init__(self, id, name, color = None, description = None, smart_tag = None, locked = None):
        self.id = id
        self.name = name
        self.color = color
        self.description = description
        self.smart_tag = smart_tag
        self.locked = locked

    def to_string(self) -> str:
        return f"ID: {self.id}\nName: {self.name}\nColor: {self.color}\nDescription: {self.description}\nSmart Tag: {self.smart_tag}\nLocked: {self.locked}\n"
