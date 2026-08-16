from classes.data.conditions import Conditions, Condition
class Field:
    """A class for storing fields in memory.
    """
    def __init__(self, name: str, applicable_conditions: list[Condition], searchable: bool, filterable: bool, orderable: bool):
        """Creates a new Field object.

        Args:
            name (str): The field's name.
            applicable_conditions (list[Condition]): A list of conditions applicable to the field.
            searchable (bool): Whether or not the field can be searched.
            filterable (bool): Whether or not the field can be filtered.
            orderable (bool): Whether or not the field can be ordered.
        """
        self.name: str = name
        self.applicable_conditions: list[Condition] = applicable_conditions
        self.searchable: bool = searchable
        self.filterable: bool = filterable
        self.orderable: bool = orderable

    def is_applicable(self, condition: Condition) -> bool:
        """Checks if a condition is applicable to the field.

        Args:
            condition (Condition): The condition to be checked.

        Returns:
            bool: Whether or not the condition is applicable to the field.
        """
        if condition in self.applicable_conditions:
            return True
        return False

class Fields:
    """A static class for storing predefined Field objects.
    """
    user_name: Field = Field(name = "user_name", applicable_conditions = [], searchable = True, filterable = False, orderable = True)
    email: Field = Field(name = "email", applicable_conditions = [], searchable = True, filterable = False, orderable = True)
    employee_id: Field = Field(name = "employee_id", applicable_conditions = [], searchable = True, filterable = False, orderable = True)
    position: Field = Field(name = "position", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = False)
    department: Field = Field(name = "department", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = False)
    manager_name: Field = Field(name = "manager_name", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = False)
    manager_email: Field = Field(name = "manager_email", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = False)
    user_location: Field = Field(name = "user_location", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = False)

    asset_name: Field = Field(name = "asset_name", applicable_conditions = [], searchable = True, filterable = False, orderable = True)
    owner_name: Field = Field(name = "owner_name", applicable_conditions = [], searchable = True, filterable = False, orderable = True)
    serial: Field  = Field(name = "serial", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = True)
    created_at: Field = Field(name = "created_at", applicable_conditions = [Conditions.after, Conditions.before, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = True)
    reported_at: Field = Field(name = "reported_at", applicable_conditions = [Conditions.after, Conditions.before, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = True)
    updated_at: Field = Field(name = "updated_at", applicable_conditions = [Conditions.after, Conditions.before, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = True)
    status: Field = Field(name = "status", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = False)
    asset_location: Field = Field(name = "asset_location", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = False)
    acquisition_price: Field = Field(name = "acquisition_price", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.greater_than, Conditions.lesser_than, Conditions.greater_than_or_equal_to, Conditions.lesser_than_or_equal_to], searchable = False, filterable = True, orderable = True)
    acquisition_date: Field = Field(name = "acquisition_date", applicable_conditions = [Conditions.before, Conditions.after, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = True)
    vendor: Field = Field(name = "vendor", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = False)
    residual_value: Field = Field(name = "residual_value", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.greater_than, Conditions.lesser_than, Conditions.greater_than_or_equal_to, Conditions.lesser_than_or_equal_to], searchable = False, filterable = True, orderable = False)
    actual_price: Field = Field(name = "actual_price", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.greater_than, Conditions.lesser_than, Conditions.greater_than_or_equal_to, Conditions.lesser_than_or_equal_to], searchable = False, filterable = True, orderable = True)
    purchase_order: Field = Field(name = "purchase_order", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = False)
    invoice: Field = Field(name = "invoice", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = False)
    manufacturer: Field = Field(name = "manufacturer", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = False)
    model: Field = Field(name = "model", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = True, filterable = True, orderable = False)
    commercial_model: Field = Field(name = "commercial_model", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = True, filterable = True, orderable = False)
    asset_type: Field = Field(name = "asset_type", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = False)
    default_ip: Field = Field(name = "default_ip", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = False)
    mac_address: Field = Field(name = "mac_address", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = True)
    format: Field = Field(name = "format", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = False)
    owner_email: Field = Field(name = "owner_email", applicable_conditions = [Conditions.equals, Conditions.not_equal_to, Conditions.is_empty, Conditions.is_not_empty], searchable = False, filterable = True, orderable = False)


