from classes.invgate.invgate_object import InvgateObject
from classes.invgate.invgate_manufacturer import InvgateManufacturer

class InvgateSoftware(InvgateObject):
    """
    A class for storing Invgate Software objects in memory. Inherits from the InvgateObject class.
    """
    def __init__(self, id: int, resource_type: str, install_date: str, install_path: str, uninstall_call: str, computer: int, version: InvgateVersion):
        """Creates a new InvgateSoftware object.

        Args:
            id (int): The software's ID.
            resource_type (str): The software's resource type.
            install_date (str): When the software was installed.
            install_path (str): Where the software is installed.
            uninstall_call (str): The call for the software to be uninstalled.
            computer (int): The computer the software is installed on.
            version (InvgateVersion): The software's version.
        """
        self.id: int = id
        self.resource_type: str = resource_type
        self.install_date: str = install_date
        self.install_path: str = install_path
        self.uninstall_call: str = uninstall_call
        self.computer: int = computer
        self.version: InvgateVersion = version
    
class InvgateVersion(InvgateObject):
    """A class for storing InvgateVersion objects in memory. Inherits from the InvgateObject class.
    """
    def __init__(self, version: str, internal_version: str, edition: str, program: InvgateProgram):
        """Creates a new InvgateVersion object.

        Args:
            version (str): The software's version.
            internal_version (str): The software's internal version.
            edition (str): The software's edition.
            program (InvgateProgram): The software program.
        """
        self.version: str = version
        self.internal_version: str = internal_version
        self.edition: str = edition
        self.program: InvgateProgram = program
        
class InvgateProgram(InvgateObject):
    """A class for storing InvgateProgram objects in memory. Inherits from the InvgateObject class.
    """
    def __init__(self, name: str, license: str, category: str, types: str, types_key: str, tags: str, is_metering_enabled: bool, manufacturer: InvgateManufacturer):
        """Creates a new InvgateProgram object.

        Args:
            name (str): The program's name.
            license (str): The program's license.
            category (str): The program's category.
            types (str): The program's types.
            types_key (str): The program's types key.
            tags (str): The program's tags.
            is_metering_enabled (bool): The program's description.
            manufacturer (InvgateManufacturer): The program's manufacturer.
        """
        
        self.name: str = name
        self.license: str = license
        self.category: str = category
        self.types: str = types
        self.types_key: str = types_key
        self.tags: str = tags
        self.is_metering_enabled: bool = is_metering_enabled
        self.manufacturer: InvgateManufacturer = manufacturer