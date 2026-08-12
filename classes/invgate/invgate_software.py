from classes.invgate.invgate_manufacturer import InvgateManufacturer

class InvgateSoftware:
    """
    A class for storing Invgate Software objects in memory.
    """
    def __init__(self, id: int, resource_type: str, install_date: str, install_path: str, uninstall_call: str, computer: int, version: InvgateVersion, program: InvgateProgram, manufacturer: InvgateManufacturer):
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
        self.version: InvgateVersion = version
        self.program: InvgateProgram = program
        self.manufacturer: InvgateManufacturer = manufacturer

    def to_string(self) -> str:
        """
        Exports the object's properties as a formatted string.
        
        Arguments:
            None:

        Returns:
            string (str): The object's properties as a formatted string.
        """

    
class InvgateVersion:
    def __init__(self, version: str, internal_version: str, edition: str):
        self.version: str = version
        self.internal_version: str = internal_version
        self.edition: str = edition
        
class InvgateProgram:
    def __init__(self, name: str, license: str, category: str, types: str, types_key: str, tags: list, is_metering_enabled: bool):
        self.name: str = name
        self.license: str = license
        self.category: str = category
        self.types: str = types
        self.types_key: str = types_key
        self.tags: list = tags
        self.is_metering_enabled: bool = is_metering_enabled