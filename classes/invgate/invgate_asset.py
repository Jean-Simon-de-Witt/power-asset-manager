from classes.invgate.invgate_status import InvgateStatus
from classes.invgate.invgate_location import InvgateLocation
from classes.invgate.invgate_user import InvgateUser
from classes.invgate.invgate_finance import InvgateFinance
from classes.invgate.invgate_manufacturer import InvgateManufacturer
from classes.invgate.invgate_health import InvgateHealth

class InvgateAsset:
    def __init__(self, name: str, id: int = None, serial: str = None, inventory_id: str = None, asset_physical_tag: str = None, created_at: str = None, reported_at: str = None, updated_at: str = None, status: InvgateStatus = None, location: InvgateLocation = None, owner: InvgateUser = None, finance: InvgateFinance = None, manufacturer: InvgateManufacturer = None, model: str = None, commercial_model: str = None, asset_type: str = None, default_ip: str = None, mac_address: str = None, asset_type_code: str = None, format: str = None, health: InvgateHealth = None):
        self.id = id
        self.name = name
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
        self.manufacturer = manufacturer
        self.model = model
        self.commercial_model = commercial_model
        self.asset_type = asset_type
        self.default_ip = default_ip
        self.mac_address = mac_address
        self.asset_type_code = asset_type_code
        self.format = format
        self.health = health

    def to_string(self):
        string = f"ID: {self.id}\n"
        string += f"Name: {self.name}\n"
        string += f"Serial: {self.serial}\n"
        string += f"Inventory ID: {self.inventory_id}\n"
        string += f"Asset Physical Tag: {self.asset_physical_tag}\n"
        string += f"Created At: {self.created_at}\n"
        string += f"Reported At: {self.reported_at}\n"
        string += f"Updated At: {self.updated_at}\n"

        if self.status:
            string += "Status:\n"
            string += f"\tID: {self.status.id}\n"
            string += f"\tName: {self.status.name}\n"
            string += f"\tDescription {self.status.description}\n"
            string += f"\tBehavior: {self.status.behavior}\n"
            string += f"\nIs Default: {self.status.is_default}"
        else:
            string += "Status: None"

        if self.location:
            string += "Location:\n"
            string += f"\tID: {self.location.id}\n"
            string += f"\tName: {self.location.name}\n"
            string += f"\tFull Path: {self.location.full_path}\n"
            string += f"\tDescription: {self.location.description}\n"
        else:
            string += "Location: None\n"

        if self.owner:
            string += "Owner:\n"
            string += f"\tID: {self.owner.id}\n"
            string += f"\tName: {self.owner.name}\n"
            string += f"\tEmail: {self.owner.email}\n"
            string += f"\tDate of Birth: {self.owner.date_of_birth}\n"
            string += f"\tEmployee ID: {self.owner.employee_id}\n"
            string += f"\tPosition: {self.owner.position}\n"
            string += f"\tDepartment: {self.owner.department}\n"
            string += f"\tCompany: {self.owner.company}\n"
            string += f"\tPhone: {self.owner.phone}\n"
            string += f"\tCellphone: {self.owner.cellphone}\n"
            string += f"\tAddress: {self.owner.address}\n"
            string += f"\tPerson Type: {self.owner.person_type}\n"
            string += f"\tUser: {self.owner.user}"
            string += f"\tManager ID: {self.owner.manager.id}\n"
            string += f"\tLocation ID: {self.owner.location.id}\n"
            string += f"\tCost Center: {self.owner.cost_center}\n"
        else:
            string += "Owner: None\n"