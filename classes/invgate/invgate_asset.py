from classes.invgate.invgate_status import InvgateStatus
from classes.invgate.invgate_location import InvgateLocation
from classes.invgate.invgate_user import InvgateUser
from classes.invgate.invgate_finance import InvgateFinance
from classes.invgate.invgate_manufacturer import InvgateManufacturer
from classes.invgate.invgate_health import InvgateHealth
from classes.invgate.invgate_software import InvgateSoftware
from classes.invgate.invgate_operating_system_update import InvgateOperatingSystemUpdate

class InvgateAsset:
    """
    A class for storing Invgate Assets in memory.
    """
    def __init__(self, name: str, id: int = None, serial: str = None, inventory_id: str = None, asset_physical_tag: str = None, created_at: str = None, reported_at: str = None, updated_at: str = None, status: InvgateStatus = None, location: InvgateLocation = None, owner: InvgateUser = None, finance: InvgateFinance = None, manufacturer: InvgateManufacturer = None, model: str = None, commercial_model: str = None, asset_type: str = None, default_ip: str = None, mac_address: str = None, asset_type_code: str = None, format: str = None):
        """
        Creates a new InvgateAsset object.
        
        Arguments:
            name* (str): The asset's name.
            id (int): The unique identifier for each asset object.
            serial (str): The asset's serial number.
            inventory_id (str): The asset's inventory ID.
            asset_physical_tag (str): The asset's physical tag.
            created_at (str): When the asset was created.
            reported_at (str): When the asset was last reported.
            updated_at (str): When the asset was last updated.
            status (InvgateStatus): The asset's status.
            location (InvgateLocation): The asset's location.
            owner (InvgateUser): The asset's owner.
            finance (InvgateFinance): The asset's finance.
            manufacturer (InvgateManufacturer): The asset's manufacturer.
            model (str): The asset's model.
            commercial_model (str): The asset's commercial model.
            asset_type (str): The asset's type.
            default_ip (str): The asset's default IP address.
            mac_address (str): The asset's MAC address.
            asset_type_code (str): Code used to represent the asset's type.
            format (str): The asset's format.

        Returns:
            None:
        """
        self.id: int = id
        self.name: str = name
        self.serial: str = serial
        self.inventory_id:str = inventory_id
        self.asset_physical_tag:str = asset_physical_tag
        self.created_at: str = created_at
        self.reported_at: str = reported_at
        self.updated_at: str = updated_at
        self.status: InvgateStatus = status
        self.location: InvgateLocation = location
        self.owner: InvgateUser = owner
        self.finance: InvgateFinance = finance
        self.manufacturer: InvgateManufacturer = manufacturer
        self.model: str = model
        self.commercial_model: str = commercial_model
        self.asset_type: str = asset_type
        self.default_ip: str = default_ip
        self.mac_address: str = mac_address
        self.asset_type_code: str = asset_type_code
        self.format: str = format

    def populate_collections(self, health: InvgateHealth = None, software: list[InvgateSoftware] = None, operating_system_updates: list[InvgateOperatingSystemUpdate] = None):
        """
        Populates the asset's collections with the provided data.
        
        Arguments:
            health (InvgateHealth): The asset's health.
            software (list[InvgateSoftware]): The asset's installed software.
            operating_system_updates (list[InvgateOperatingSystemUpdate]): The asset's operating system updates.

        Returns:
            None:
        """
        if health:
            self.health: InvgateHealth = health

        if software:
            self.software: list[InvgateSoftware] = []
            for s in software:
                self.software.append(s)

        if operating_system_updates:
            self.operating_system_updates: list[InvgateOperatingSystemUpdate] = []
            for os_update in operating_system_updates:
                self.operating_system_updates.append(os_update)

    def to_string(self) -> str:
        """
        Exports the object's properties as a formatted string.
        
        Arguments:
            None:

        Returns:
            string (str): The object's properties as a formatted string.
        """
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
            string += f"\tDescription: {self.status.description}\n"
            string += f"\tBehavior: {self.status.behavior}\n"
            string += f"\tIs Default: {self.status.is_default}\n"
        else:
            string += "Status: None\n"

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
            string += f"\tUser: {self.owner.user}\n"
            string += f"\tCost Center: {self.owner.cost_center}\n"
        else:
            string += "Owner: None\n"

        if self.finance:
            string += "Finance:\n"
            string += f"\tID: {self.finance.id}\n"
            string += f"\tAsset ID: {self.finance.asset}\n"
            string += f"\tAcquisition Type: {self.finance.acquisition_type}\n"
            string += f"\tAcquisition Date: {self.finance.acquisition_date}\n"
            string += f"\tAcquisition Price: {self.finance.acquisition_price}\n"
            string += f"\tActual Price: {self.finance.actual_price}\n"
            string += f"\tResidual Value: {self.finance.residual_value}\n"
            string += f"\tDepreciation Percentage: {self.finance.depreciation_percentage}\n"
            string += f"\tWarranty Date: {self.finance.warranty_date}\n"
            string += f"\tCost Center: {self.finance.cost_center}\n"
            string += f"\tInvoice ID: {self.finance.invoice_id}\n"
        else:
            string += "Finance: None\n"

        if self.manufacturer:
            string += "Manufacturer:\n"
            string += f"\tID: {self.manufacturer.id}\n"
            string += f"\tName: {self.manufacturer.name}\n"

        else:
            string += "Manufacturer: None\n"
        string += f"Model: {self.model}\n"
        string += f"Commercial Model: {self.commercial_model}\n"
        string += f"Asset Type: {self.asset_type}\n"
        string += f"Default IP: {self.default_ip}\n"
        string += f"MAC Address: {self.mac_address}\n"
        string += f"Asset Type Code: {self.asset_type_code}\n"
        string += f"Format: {self.format}\n"

        if hasattr(self, "software"):
            string += f"Software Installed: {len(self.software)}\n"
        else:
            string += "Software Installed: None\n"

        if hasattr(self, "operating_system_updates"):
            string += f"Operating System Updates: {len(self.operating_system_updates)}\n"
        else:
            string += "Operating System Updates: None\n"
        return string  

    def to_json(self, include_id: bool = False) -> dict:
        """
        Exports the object's properties as a JSON object.
        
        Arguments:
            None:
        
        Returns:
            json (dict): The object's properties as a JSON object.
        """
        json = {}

        if self.id and include_id:
            json["id"] = self.id

        if self.name:
            json["name"] = self.name

        if self.serial:
            json["serial"] = self.serial

        if self.inventory_id:
            json["inventory_id"] = self.inventory_id

        if self.asset_physical_tag:
            json["asset_physical_tag"] = self.asset_physical_tag

        if self.created_at:
            json["created_at"] = self.created_at

        if self.reported_at:
            json["reported_at"] = self.reported_at

        if self.updated_at:
            json["updated_at"] = self.updated_at

        if self.status:
            json["status"] = self.status.id

        if self.location:
            json["location"] = self.location.id

        if self.owner:
            json["owner"] = self.owner.id

        if self.finance:
            json["finance"] = self.finance.id

        if self.manufacturer:
            json["manufacturer"] = self.manufacturer.name

        if self.model:
            json["model"] = self.model

        if self.commercial_model:
            json["commercial_model"] = self.commercial_model

        if self.asset_type:
            json["asset_type"] = self.asset_type

        if self.default_ip:
            json["default_ip"] = self.default_ip

        if self.mac_address:
            json["mac_address"] = self.mac_address

        if self.asset_type_code:
            json["asset_type_code"] = self.asset_type_code

        if self.format:
            json["format"] = self.format

        return json