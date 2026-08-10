from classes.data.fields import Fields, Field
class Collection:
    def __init__(self, name: str, contained_fields: list[Field]):
        self.name: str = name
        self.contained_fields: list[Field] = contained_fields

class Collections:
    users: Collection = Collection(name = "users", contained_fields = [Fields.user_name, Fields.email, Fields.employee_id, Fields.position, Fields.department, Fields.manager_name, Fields.manager_email, Fields.user_location])
    assets: Collection = Collection(name = "assets", contained_fields = [Fields.asset_name, Fields.serial, Fields.created_at, Fields.reported_at, Fields.updated_at, Fields.status, Fields.owner_name, Fields.owner_email, Fields.asset_location, Fields.model, Fields.commercial_model, Fields.default_ip, Fields.mac_address, Fields.purchase_order, Fields.invoice, Fields.manufacturer, Fields.asset_type, Fields.format, Fields.acquisition_price, Fields.acquisition_date, Fields.vendor, Fields.residual_value, Fields.actual_price])