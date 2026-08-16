class InvgateObject:
    """The parent class for all Invgate object types.
    """
    def to_string(self, indent: int = 0) -> str:
        """Exports the object's properties as a formatted string.

        Args:
            indent (int, optional): Specifies how many tab spaces the string is indented by. Defaults to 0.

        Returns:
            str: The object's properties as a formatted string.
        """
        attributes: dict = vars(self)
        string = ""
        for name, value in attributes.items():
            if name.startswith("__") or not value:
                continue

            if type(value) in [str, int, float, bool]:
                string += f"{'\t' * indent}{name.replace('_', ' ').title()}: {value}\n"
            elif type(value) == list:
                string += f"{'\t' * indent}{name.replace('_', ' ').title()} Count: {len(value)}"
            else:
                string += f"{'\t' * indent}{name.replace('_', ' ').title()}:\n"
                string += value.to_string(indent = indent + 1)
        return string