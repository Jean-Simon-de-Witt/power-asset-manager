class InvgateHealth:
    def __init__(self, computer, updated_at = None, health_rule = None, status = None):
        self.computer = computer
        self.updated_at = updated_at
        self.health_rule = health_rule
        self.status = status

    def to_string(self):
        return f"Computer: {self.computer}\nUpdated At: {self.updated_at}\nHealth Rule: {self.health_rule}\nStatus: {self.status}\n"