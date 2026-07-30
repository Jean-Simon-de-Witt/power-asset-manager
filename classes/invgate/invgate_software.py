from classes.invgate.invgate_manufacturer import InvgateManufacturer

class InvgateSoftware:
    def __init__(self, id: int, resource_type: str = None, install_date: str = None, install_path: str = None, uninstall_call: str = None, computer: int = None, version: str = None, internal_version: str = None, edition: str = None, name: str = None, manufacturer: InvgateManufacturer = None, license: str = None, category: str = None, types: str = None, types_key: str = None, tags: list = None, is_metering_enabled: bool = False):
        self.id: int = id
        self.resource_type: str = resource_type
        self.install_date: str = install_date
        self.install_path: str = install_path
        self.uninstall_call: str = uninstall_call
        self.computer: int = computer
        self.version: str = version
        self.internal_version: str = internal_version
        self.edition: str = edition
        self.name: str = name
        self.manufacturer: InvgateManufacturer = manufacturer
        self.license: str = license
        self.category: str = category
        self.types: str = types
        self.types_key: str = types_key
        self.tags: list = list
        self.is_metering_enabled: bool = is_metering_enabled

    def to_string(self) -> str:
        string = f"ID: {self.id}\n"
        string += f"Resource Type: {self.resource_type}\n"
        string += f"Install Date: {self.install_date}\n"
        string += f"Install Path: {self.install_path}\n"
        string += f"Uninstall Call: {self.uninstall_call}\n"
        string += f"Computer ID: {self.computer}\n"
        string += f"Version: {self.version}\n"
        string += f"Internal Version: {self.internal_version}\n"
        string += f"Edition: {self.edition}\n"
        string += f"Name: {self.name}\n"

        if self.manufacturer:
            string += "Manufacturer:\n"
            string += f"\tID: {self.manufacturer.id}\n"
            string += f"\tName: {self.manufacturer.name}\n"
        else:
            string += "Manufacturer: None\n"
        string += f"License: {self.license}\n"
        string += f"Category: {self.category}\n"
        string += f"Types: {self.types}\n"
        string += f"Types Key: {self.types_key}\n"
        string += f"Tags: {self.tags}\n"
        string += f"Is Metering Enabled: {self.is_metering_enabled}\n"
        return string