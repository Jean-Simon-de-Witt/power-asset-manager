class Condition:
    """A class for storing conditions in memory.
    """
    def __init__(self, name: str, symbol: str):
        """Creates a new Condition object.

        Args:
            name (str): The condition's name.
            symbol (str): The condition's symbol.
        """
        
        self.name: str = name
        self.symbol: str = symbol
        self.inverse: Condition = None
        self.apply = None

class Conditions:
    """A static class for storing predefined Condition objects.
    """
    
    equals: Condition = Condition(name = "equals", symbol = "==")
    not_equal_to: Condition = Condition(name = "not_equal_to", symbol = "!=")
    greater_than: Condition = Condition(name = "greater_than", symbol = ">")
    lesser_than: Condition = Condition(name = "lesser_than", symbol = "<")
    after: Condition = Condition(name = "after", symbol = ">")
    before: Condition = Condition(name = "before", symbol = "<")
    greater_than_or_equal_to: Condition = Condition(name = "greater_than_or_equal_to", symbol = ">=")
    lesser_than_or_equal_to: Condition = Condition(name = "lesser_than_or_equal_to", symbol = "<=")
    is_empty: Condition = Condition(name = "is_empty", symbol = "not")
    is_not_empty: Condition = Condition(name = "is_not_empty", symbol = "is not None")

    equals.inverse = not_equal_to
    not_equal_to.inverse = equals
    greater_than.inverse = lesser_than
    lesser_than.inverse = greater_than
    after.inverse = before
    before.inverse = after
    greater_than_or_equal_to.inverse = lesser_than_or_equal_to
    lesser_than_or_equal_to.inverse = greater_than_or_equal_to
    is_empty.inverse = is_not_empty
    is_not_empty.inverse = is_empty

    equals.apply = lambda value1, value2: value1 == value2
    not_equal_to.apply = lambda value1, value2: value1 != value2
    greater_than.apply = lambda value1, value2: value1 > value2
    lesser_than.apply = lambda value1, value2: value1 < value2
    after.apply = lambda value1, value2: value1 > value2
    before.apply = lambda value1, value2: value1 < value2
    greater_than_or_equal_to.apply = lambda value1, value2: value1 >= value2
    lesser_than_or_equal_to.apply = lambda value1, value2: value1 <= value2
    is_empty.apply = lambda value1, value2 = None: not value1
    is_not_empty.apply = lambda value1, value2 = None: value1 is not None