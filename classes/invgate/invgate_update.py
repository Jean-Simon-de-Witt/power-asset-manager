from classes.invgate.invgate_object import InvgateObject

class InvgateUpdate(InvgateObject):
    """A class for storing InvgateUpdate objects in memory. Inherits from the InvgateObject class.
    """
    def __init__(self, id: int, install_date: str, status: str, computer: int, operating_system_update_version: InvgateOperatingSystemUpdateVersion):
        """Creates a new InvgateUpdate object.

        Args:
            id (int): The update's id.
            install_date (str): When the update was installed.
            status (str): The update's status.
            computer (int): The computer the update is installed on.
            operating_system_update_version (InvgateOperatingSystemUpdateVersion): The update's version.
        """
        self.id: int = id
        self.install_date: str = install_date
        self.status: str = status
        self.computer: int = computer
        self.operating_system_update_version: InvgateOperatingSystemUpdateVersion = operating_system_update_version

class InvgateOperatingSystemUpdateVersion(InvgateObject):
    """A class for storing InvgateSystemUpdateVersion objects in memory. Inherits from the InvgateObject class.
    """
    def __init__(self, version: str, release_date: str, operating_system_update: InvgateOperatingSystemUpdate):
        """Creates a new InvgateOperatingSystemUpdateVersion object.

        Args:
            version (str): The update's version.
            release_date (str): When the version was released.
            operating_system_update (InvgateOperatingSystemUpdate): The version's operating system update.
        """
        self.version: str = version
        self.release_date: str = release_date
        self.operating_system_update: InvgateOperatingSystemUpdate = operating_system_update

class InvgateOperatingSystemUpdate(InvgateObject):
    """A class for storing InvgateOperatingSystemUpdate objects in memory. Inherits from the InvgateObject class.
    """
    def __init__(self, short_name: str, name: str, update_type: str, os_type: str, severity: str, support_url: str):
        """Creates a new InvgateOperatingSystemUpdate object.

        Args:
            short_name (str): The update's short name.
            name (str): The update's name.
            update_type (str): The update's type.
            os_type (str): The operating system's type.
            severity (str): The update's severity.
            support_url (str): The update's support URL.
        """
        self.short_name: str = short_name
        self.name: str = name
        self.update_type: str = update_type
        self.os_type: str = os_type
        self.severity: str = severity
        self.support_url: str = support_url