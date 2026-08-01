from classes.invgate.invgate_manufacturer import InvgateManufacturer

class InvgateSoftware:
    """
    A class for storing Invgate Software objects in memory.
    """
    def __init__(self, id: int, resource_type: str = None, install_date: str = None, install_path: str = None, uninstall_call: str = None, computer: int = None, version: str = None, internal_version: str = None, edition: str = None, name: str = None, manufacturer: InvgateManufacturer = None, license: str = None, category: str = None, types: str = None, types_key: str = None, tags: list = None, is_metering_enabled: bool = False):
        """
        Creates a new InvgateSoftware object.
        
        Arguments:
            id* (int): The unique identifier for each software object.
            respurce_type (str): The subtype of the installed program.
            install_date (str): Date when the program was installed.
            install_path (str): Where the program is installed.
            uninstall_call (str): Command used to uninstall the program using Windows.
            computer (int): The unique identifier linking to the asset's ID.
            version (str): The software's version.
            internal_version (str): The software's internal version.
            edition (str): The software's edition.
            name (str): The software's name.
            manufacturer (InvgateManufacturer): The software's manufacturer.
            license (str): The software's license type.
            category (str): The software's category.
            types (str): The program's type.
            types_key (str): The program's type key.
            tags (list): The program's tags.
            is_metering_enabled (bool): Whether or not usage metering is enabled.

        Returns:
            None:
        """
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
        """
        Exports the object's properties as a formatted string.
        
        Arguments:
            None:

        Returns:
            string (str): The object's properties as a formatted string.
        """
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