from classes.invgate.invgate_finance import InvgateFinance
from classes.invgate.invgate_user import InvgateUser

class InvgateAsset:
    def __init_(self, name, id = None, serial = None, inventory_id = None, asset_physical_tag = None, created_at = None, reported_at = None, updated_at = None, status = None, location = None, owner: InvgateUser = None, finance: InvgateFinance = None, sources = None, manufacturer = None, model = None, commercial_model = None, asset_type = None, default_ip = None, mac_address = None, asset_type_code = None, format = None):
        self.name = name
        self.id = id
        self.serial = serial
        self.inventory_id = inventory_id
        self.asset_physical_tag = asset_physical_tag
        self.created_at = created_at
        self.reported_at = reported_at
        self.updated_at = updated_at
        self.status = status
        self.location = location
        self.owner = owner
        self.finance = finance
        self.sources = sources
        self.manufacturer = manufacturer
        self.model = model
        self.commercial_model = commercial_model
        self.asset_type = asset_type
        self.default_ip = default_ip
        self.mac_address = mac_address
        self.asset_type_code = asset_type_code
        self.format = format