class InvgateObject:
    def to_string(self, indent: int = 0):
        attributes: dict = vars(self)
        string = ""
        for name, value in attributes.items():
            if name.startswith("__") or not value:
                continue

            if type(value) in [str, int, float, bool]:
                string += f"{"\t" * indent}{name.replace("_", " ").title()}: {value}\n"
            else:
                string += f"{"\t" * indent}{name.replace("_", " ").title()}:\n"
                string += value.to_string(indent = indent + 1)
        return string