class InvgateUpdate:
    def __init__(self, id: int, install_date: str, status: str, computer: int, operating_system_update_version: InvgateOperatingSystemUpdateVersion):
        self.id: int = id
        self.install_date: str = install_date
        self.status: str = status
        self.computer: int = computer

class InvgateOperatingSystemUpdateVersion:
    def __init__(self, version: str, release_date: str, operating_system_update: InvgateOperatingSystemUpdate):
        self.version: str = version
        self.release_date: str = release_date
        self.operating_system_update: InvgateOperatingSystemUpdate = operating_system_update

class InvgateOperatingSystemUpdate:
    def __init__(self, short_name: str, name: str, update_type: str, os_type: str, severity: str, support_url: str):
        self.short_name: str = short_name
        self.name: str = name
        self.update_type: str = update_type
        self.os_type: str = os_type
        self.os_type: str = os_type
        self.severity: str = severity
        self.support_url: str = support_url