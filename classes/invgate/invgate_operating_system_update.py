class InvgateOperatingSystemUpdate:
    """
    A class for storing Invgate Operating System Update objects in memory.
    """
    def __init__(self, id: int, install_date: str = None, status: str = None, computer: int = None, version: str = None, release_date: str = None, short_name: str = None, name: str = None, update_type: str = None, os_type: str = None, severity: str = None, support_url: str = None):
        """
        Creates a new InvgateOperatingSystemUpdate object.
        
        Arguments:
            id* (int): The unique identifier for each operating system update object.
            install_date (str): The date at which the updated was installed.
            status (str): The installation's status.
            computer (int): The unique identifier linking to the asset's ID.
            version (str): The update's version.
            release_date (str): The update's release date.
            short name (str): The update's short name.
            name (str): The update's name.
            update_type (str): The type of update.
            os_type (str): The type of operating system.
            severity (str): The importance of the update.
            support_url (str): The update's support URL.

        Returns:
            None:
        """
        self.id: int = id
        self.install_date: str = install_date
        self.status: str = status
        self.computer: int = computer
        self.version: str = version
        self.release_date: str = release_date
        self.short_name: str = short_name
        self.name: str = name
        self.update_type: str = update_type
        self.os_type: str = os_type
        self.severity: str = severity
        self.support_url: str = support_url

    def to_string(self) -> str:
        """
        Exports the object's properties as a formatted string.
        
        Arguments:
            None:

        Returns:
            string (str): The object's properties as a formatted string.
        """
        string = f"ID: {self.id}\n"
        string += f"Install Date: {self.install_date}\n"
        string += f"Status: {self.status}\n"
        string += f"Computer ID: {self.computer}\n"
        string += f"Version: {self.version}\n"
        string += f"Release Date: {self.release_date}\n"
        string += f"Short Name: {self.short_name}\n"
        string += f"Name: {self.name}\n"
        string += f"Update Type: {self.update_type}\n"
        string += f"OS Type: {self.os_type}\n"
        string += f"Severity: {self.severity}\n"
        string += f"Support URL: {self.support_url}\n"
        return string