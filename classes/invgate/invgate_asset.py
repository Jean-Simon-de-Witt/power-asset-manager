from classes.invgate.invgate_object import InvgateObject
from classes.invgate.invgate_status import InvgateStatus
from classes.invgate.invgate_location import InvgateLocation
from classes.invgate.invgate_user import InvgateUser
from classes.invgate.invgate_finance import InvgateFinance
from classes.invgate.invgate_manufacturer import InvgateManufacturer
from classes.invgate.invgate_health import InvgateHealth
from classes.invgate.invgate_software import InvgateSoftware
from classes.invgate.invgate_update import InvgateUpdate

class InvgateAsset(InvgateObject):
    """A class for storing InvgateAsset objects in memory. Inherits from the InvgateObject class.
    """
    def __init__(self, id: int, name: str, manufacturer: InvgateManufacturer, model: str, commercial_model: str, serial: str, inventory_id: int, asset_physical_tag: str, physical_identifier_epc: str, created_at: str, reported_at: str, updated_at: str, finance: InvgateFinance, asset_type: str, asset_type_code: str, owner: InvgateUser, location: InvgateLocation, status: InvgateStatus, default_ip: str, mac_address: str, format: str):
        """Creates a new InvgateAsset object.

        Args:
            id (int): The asset's ID.
            name (str): The asset's name.
            manufacturer (InvgateManufacturer): The asset's manufacturer.
            model (str): The asset's model.
            commercial_model (str): The asset's commercial model.
            serial (str): The asset's serial number.
            inventory_id (int): The asset's inventory ID.
            asset_physical_tag (str): The asset's physical tag.
            physical_identifier_epc (str): The asset's physical identifier.
            created_at (str): When the asset was created.
            reported_at (str): When the asset was last reported.
            updated_at (str): When the asset was last updated.
            finance (InvgateFinance): The asset's finance.
            asset_type (str): The asset's type.
            asset_type_code (str): The asset's type code.
            owner (InvgateUser): The asset's owner.
            location (InvgateLocation): The asset's location.
            status (InvgateStatus): The asset's status.
            default_ip (str): The asset's default IPv4 address.
            mac_address (str): The asset's MAC address.
            format (str): The asset's format.
        """
        
        self.id: int = id
        self.name: str = name
        self.manufacturer: InvgateManufacturer = manufacturer
        self.model: str = model
        self.commercial_model: str = commercial_model
        self.serial: str = serial
        self.inventory_id: int = inventory_id
        self.asset_physical_tag: str = asset_physical_tag
        self.physical_identifier_epc: str = physical_identifier_epc
        self.created_at: str = created_at
        self.reported_at: str = reported_at
        self.updated_at: str = updated_at
        self.finance: InvgateFinance = finance
        self.asset_type: str = asset_type
        self.asset_type_code: str = asset_type_code
        self.owner: InvgateUser = owner
        self.location: InvgateLocation = location
        self.status: InvgateStatus = status
        self.default_ip: str = default_ip
        self.mac_address: str = mac_address
        self.format: str = format

    def populate_collections(self, health: InvgateHealth = None, software: list[InvgateSoftware] = None, updates: list[InvgateUpdate] = None):
        """Populates the asset's collection attributes with the given data.

        Args:
            health (InvgateHealth, optional): The asset's health. Not populated if None. Defaults to None.
            software (list[InvgateSoftware], optional): The asset's software. Not populated if None. Defaults to None.
            updates (list[InvgateUpdate], optional): The asset's updates. Not populated if None. Defaults to None.
        """
        
        if health:
            self.health: InvgateHealth = health

        if software:
            self.software: list[InvgateSoftware] = []
            for s in software.get("software"):
                self.software.append(s)

        if updates:
            self.operating_system_updates: list[InvgateUpdate] = []
            for os_update in updates.get("updates"):
                self.operating_system_updates.append(os_update)

    def to_json(self, include_id: bool = False) -> dict:
        """Exports the asset's properties as a JSON object for performing POST and PATCH requests

        Args:
            include_id (bool, optional): Whether or not to export the ID. Defaults to False. Defaults to False.

        Returns:
            dict: The asset's properties exported as a JSON object
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