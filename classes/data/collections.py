from classes.data.fields import Fields, Field
class Collection:
    """A class for storing collections in memory.
    """
    def __init__(self, name: str, contained_fields: list[Field]):
        """Creates a new Collection object.

        Args:
            name (str): The collection's name.
            contained_fields (list[Field]): The fields contained within the collection.
        """
        self.name: str = name
        self.contained_fields: list[Field] = contained_fields

    def contains_field(self, field: Field) -> bool:
        """Checks if the collection contains the specified field.

        Args:
            field (Field): The field to be checked.

        Returns:
            bool: Whether or not the field is contained within the collection.
        """
        if field in self.contained_fields:
            return True
        return False

class Collections:
    """A static class for storing predefined Collection objects.
    """
    users: Collection = Collection(name = "users", contained_fields = [Fields.user_name, Fields.email, Fields.employee_id, Fields.position, Fields.department, Fields.manager_name, Fields.manager_email, Fields.user_location])
    assets: Collection = Collection(name = "assets", contained_fields = [Fields.asset_name, Fields.serial, Fields.created_at, Fields.reported_at, Fields.updated_at, Fields.status, Fields.owner_name, Fields.owner_email, Fields.asset_location, Fields.model, Fields.commercial_model, Fields.default_ip, Fields.mac_address, Fields.purchase_order, Fields.invoice, Fields.manufacturer, Fields.asset_type, Fields.format, Fields.acquisition_price, Fields.acquisition_date, Fields.vendor, Fields.residual_value, Fields.actual_price])