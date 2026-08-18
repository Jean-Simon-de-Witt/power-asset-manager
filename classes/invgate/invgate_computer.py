from classes.invgate.invgate_object import InvgateObject
from classes.invgate.invgate_asset import InvgateAsset

# ===========================================================================
# Manufacturer
# ===========================================================================

class ReportedManufacturer(InvgateObject):
    """A class for storing reported manufacturer data in memory. Inherits from the InvgateObject class. 
    """
    
    def __init__(self, id: str, name: str, is_manual: bool, is_component: bool, logo: str, support_url: str, website_url: str):
        """Creates a new ReportedManufacturer object.

        Args:
            id (str): The manufacturer's ID.
            name (str): The manufacturer's name.
            is_manual (bool): Whether or not the manufacturer is manual.
            is_component (bool): Whether or not the manufacturer is a component.
            logo (str): The manufacturer's logo.
            support_url (str): The manufacturer's support URL.
            website_url (str): The manufacturer's website URL
        """
        
        self.id: str = id
        self.name: str = name
        self.is_manual: bool = is_manual
        self.is_component: bool = is_component
        self.logo: str = logo
        self.support_url: str = support_url
        self.website_url: str = website_url

# ===========================================================================
# OS Info
# ===========================================================================

class ReportedUser(InvgateObject):
    """A class for storing reported user data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, name: str, raw_username: str, current: bool, last_login_time: str):
        """Creates a new ReportedUser object.

        Args:
            name (str): The user's name.
            raw_username (str): The user's raw username.
            current (bool): Whether or not this is the current user.
            last_login_time (str): The last time the user logged in.
        """
        
        self.name: str = name
        self.raw_username: str = raw_username
        self.current: bool = current
        self.last_login_time: str = last_login_time

class ReportedNetworkAdapterModel(InvgateObject):
    """A class for storing reported network adapter model data in memory. Inherits from the InvgateObject class.
    """
    def __init__(self, id: str, model_name: str, model: str, name: str, description: str, status: str, icon: str, kind: str, sku: str, is_manual: bool, import_uuid: str, updated_at: str, device_type: str, manufacturer: ReportedManufacturer):
        """Creates a new ReportedNetworkAdapterModel object.

        Args:
            id (str): The adapter model's ID.
            model_name (str): The adapter's model name.
            model (str): The adapter's model.
            name (str): The adapter's name.
            description (str): The adapter's description.
            status (str): The adapter's status.
            icon (str): The adapter's icon.
            kind (str): The adapter's kind.
            sku (str): The adapter's sku.
            is_manual (bool): Whether or not the adapter is manual.
            import_uuid (str): The adapter's import uuid.
            updated_at (str): When last the adapter was updated.
            device_type (str): The adapter's device type.
            manufacturer (ReportedManufacturer): The adapter's manufacturer.
        """
        self.id: str = id
        self.model_name: str = model_name
        self.model: str = model
        self.name: str = name
        self.description: str = description
        self.status: str = status
        self.icon: str = icon
        self.kind: str = kind
        self.sku: str = sku
        self.is_manual: bool = is_manual
        self.import_uuid: str = import_uuid
        self.updated_at: str = updated_at
        self.device_type: str = device_type
        self.manufacturer: ReportedManufacturer = manufacturer

class ReportedOSStatus(InvgateObject):
    """A class for storing reported OS status data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, id: str, uptime: int, boot_time: str, firewall: str, usb: str, default_ip: str, antivirus: str, antivirus_name: str, memory_size: int, memory_available: int, rdp_enabled: bool, vnc_enabled: bool, teamviewer_id: int, anydesk_id: int, logged_users: list[ReportedUser]):
        """Creates a new ReportedOSStatus object.

        Args:
            id (str): The OS status' ID.
            uptime (int): The computer's uptime.
            boot_time (str): When the computer last booted.
            firewall (str): The computer's firewall status.
            usb (str): The computer's USB status.
            default_ip (str): The computer's default IP.
            antivirus (str): The computer's antivirus status.
            antivirus_name (str): The computer's antivirus name.
            memory_size (int): The computer's memory size.
            memory_available (int): The computer's memory available.
            rdp_enabled (bool): Whether or not RDP is enabled.
            vnc_enabled (bool): Whether or not VNC is enabled.
            teamviewer_id (int): The computer's TeamViewer ID.
            anydesk_id (int): The computer's AnyDesk ID.
            logged_users (list[ReportedUser]): A list of logged users on the computer.
        """
        
        self.id: str = id
        self.uptime: int = uptime
        self.boot_time: str = boot_time
        self.firewall: str = firewall
        self.usb: str = usb
        self.default_ip: str = default_ip
        self.antivirus: str = antivirus
        self.antivirus_name: str = antivirus_name
        self.memory_size: int = memory_size
        self.memory_available: int = memory_available
        self.rdp_enabled: bool = rdp_enabled
        self.vnc_enabled: bool = vnc_enabled
        self.teamviewer_id: int = teamviewer_id
        self.anydesk_id: int = anydesk_id
        self.logged_users: list[ReportedUser] = logged_users

class ReportedDomain(InvgateObject):
    """A class for storing reported domain data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, id: str, name: str):
        """Creates a new ReportedDomain object.

        Args:
            id (str): The domain's ID.
            name (str): The domain's name.
        """
        
        self.id: str = id
        self.name: str = name

class ReportedDNS(InvgateObject):
    """A class for storing reported DNS data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, id: str, ip_address: str):
        """Creates a new ReportedDNS object.

        Args:
            id (str): The DNS's ID.
            ip_address (str): The DNS's IP address.
        """
        
        self.id: str = id
        self.ip_address: str = ip_address

class ReportedGateway(InvgateObject):
    """A class for storing reported gateway data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, id: str, ip_address: str):
        """Creates a new ReportedGateway object.

        Args:
            id (str): The gateway's ID.
            ip_address (str): The gateway's IP address.
        """
        
        self.id: str = id
        self.ip_address: str = ip_address

class ReportedNetworkAdapter(InvgateObject):
    """A class for storing reported network adapter data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, id: str, device_id: str, is_virtual: bool, mac: str, speed: str, ip_address: str, ipv6_address: str, ip_netmask: str, ip_prefix: str, default: bool, nic: ReportedNetworkAdapterModel):
        """Creates a new ReportedNetworkAdapter object.

        Args:
            id (str): The network adapter's ID.
            device_id (str): Adapter's type.
            is_virtual (bool): Whether or not the adapter is virtual.
            mac (str): The adapter's MAC address.
            speed (str): The adapter's speed.
            ip_address (str): The adapter's IPv4 address.
            ipv6_address (str): The adapter's IPv6 address.
            ip_netmask (str): The adapter's IP netmask.
            ip_prefix (str): The adapter's IP prefix.
            default (bool): Whether or not the adapter is a default.
            nic (ReportedNetworkAdapterModel): The adapter's model.
        """
        self.id: str = id
        self.device_id: str = device_id
        self.is_virtual: bool = is_virtual
        self.mac: str = mac
        self.speed: str = speed
        self.ip_address: str = ip_address
        self.ipv6_address: str = ipv6_address
        self.ip_netmask: str = ip_netmask
        self.ip_prefix: str = ip_prefix
        self.default: bool = default
        self.nic: ReportedNetworkAdapterModel = nic

class ReportedOS(InvgateObject):
    """A class for storing reported OS data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, id: str, name: str, version: str, arch: str, full_name: str, supports_software_deployment: bool, manufacturer: ReportedManufacturer):
        """Creates a new ReportedOS object.

        Args:
            id (str): The OS's ID.
            name (str): The OS's name.
            version (str): The OS's version.
            arch (str): The OS's arch.
            full_name (str): The OS's full name.
            supports_software_deployment (bool): Whether or not the OS supports software deployment.
            manufacturer (ReportedManufacturer): The OS's manufacturer.
        """
        
        self.id: str = id
        self.name: str = name
        self.version: str = version
        self.arch: str = arch
        self.full_name: str = full_name
        self.supports_software_deployment: bool = supports_software_deployment
        self.manufacturer: ReportedManufacturer = manufacturer

class ReportedOSInfo(InvgateObject):
    """A class for storing reported OS info data in memory. Inherits from the InvgateObject class.
    """
    def __init__(self, id: str, serial: str, product_key: str, hostname: str, azure_ad_tenant_name: str, os: ReportedOS, network_adapters: list[ReportedNetworkAdapter], gateway: ReportedGateway, dns: ReportedDNS, domains: list[ReportedDomain], os_status: ReportedOSStatus):
        """Creates a new ReportedOSInfo object.

        Args:
            id (str): The OS info's ID.
            serial (str): The OS's serial number.
            product_key (str): The OS's product key.
            hostname (str): The computer's hostname.
            azure_ad_tenant_name (str): The Azure AD tenant name.
            os (ReportedOS): The computer's operating system.
            network_adapters (list[ReportedNetworkAdapter]): A list of the computer's network adapters.
            gateway (ReportedGateway): The computer's gateway.
            dns (ReportedDNS): The computer's DNS.
            domains (list[ReportedDomain]): A list of the computer's domains.
            os_status (ReportedOSStatus): The computer's OS status.
        """
        self.id: str = id
        self.serial: str = serial
        self.product_key: str = product_key
        self.hostname: str = hostname
        self.azure_ad_tenant_name: str = azure_ad_tenant_name
        self.os: ReportedOS = os
        self.network_adapters: list[ReportedNetworkAdapter] = network_adapters
        self.gateway: ReportedGateway = gateway
        self.dns: ReportedDNS = dns
        self.domains: list[ReportedDomain] = domains
        self.os_status: ReportedOSStatus = os_status
  
# ===========================================================================
# Geolocation
# ===========================================================================

class ReportedGeolocation(InvgateObject):
    """A class for storing reported geolocation data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, id: str, latitude: float, longitude: float):
        """Creates a new ReportedGeolocation object.

        Args:
            id (str): The geolocation's ID.
            latitude (float): The geolocation's latitude.
            longitude (float): The geolocation's longitude.
        """
        
        self.id: str = id
        self.latitude: float = latitude
        self.longitude: float = longitude

# ===========================================================================
# Motherboard
# ===========================================================================

class ReportedMotherboardModel(InvgateObject):
    """A class for storing reported motherboard model data in memory. Inherits from InvgateObject.
    """
    
    def __init__(self, id: str, model: str):
        """Creates a new ReportedMotherboardModel object.

        Args:
            id (str): The model's ID.
            model (str): The model's name.
        """
        self.id: str = id
        self.model: str = model

class ReportedMotherboard(InvgateObject):
    """A class for storing reported motherboard data in memory. Inherits from InvgateObject.
    """
    
    def __init__(self, id: str, serial: str, model: ReportedMotherboardModel):
        """Creates a new ReportedMotherboard object.

        Args:
            id (int): The motherboard's ID.
            serial (str): The motherboard's serial number.
            model (ReportedMotherboardModel): The motherboard's model.
        """
        
        self.id: str = id
        self.serial: str = serial
        self.model: ReportedMotherboardModel = model

# ===========================================================================
# CPU
# ===========================================================================

class ReportedCPUModel(InvgateObject):
    """A class for storing reported CPU model data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, id: str, model_name: str, model: str, name: str, description: str, status: str, icon: str, kind: str, sku: str, is_manual: bool, import_uuid: str, updated_at: str, family: str, frequency: str, cores: int, manufacturer: ReportedManufacturer):
        """Creates a new ReportedCPUModel object.

        Args:
            id (str): The model's ID.
            model_name (str): The model's model name.
            model (str): The model's model.
            name (str): The model's name.
            description (str): The model's description.
            status (str): The model's status.
            icon (str): The model's icon.
            kind (str): The model's kind.
            sku (str): The model's SKU.
            is_manual (bool): Whether or not the model is manual.
            import_uuid (str): The Model's import UUID.
            updated_at (str): When last the model was updated.
            family (str): The model's family.
            frequency (str): The model's frequency.
            cores (int): The model's number of cores.
            manufacturer (ReportedManufacturer): The model's manufacturer.
        """
        
        self.id: str = id
        self.model_name: str = model_name
        self.model: str = model
        self.name: str = name
        self.description: str = description
        self.status: str = status
        self.icon: str = icon
        self.kind: str = kind
        self.sku: str = sku
        self.is_manual: bool = is_manual
        self.import_uuid: str = import_uuid
        self.updated_at: str = updated_at
        self.family: str = family
        self.frequency: str = frequency
        self.cores: int = cores
        self.manufacturer: ReportedManufacturer = manufacturer

class ReportedCPU(InvgateObject):
    """A class for storing reported CPU data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, id: str, serial: str, created_at: str, deleted_at: str, assigned_cores: int, model: ReportedCPUModel):
        """Creates a new ReportedCPU object.

        Args:
            id (str): The CPU's ID.
            serial (str): The CPU's serial number.
            created_at (str): When the CPU was created.
            deleted_at (str): When the CPU was deleted.
            assigned_cores (int): How many cores the CPU is assigned.
            model (ReportedCPUModel): The CPU's model.
        """
        
        self.id: str = id
        self.serial: str = serial
        self.created_at: str = created_at
        self.deleted_at: str = deleted_at
        self.assigned_cores: int = assigned_cores
        self.model: ReportedCPUModel = model

# ===========================================================================
# RAM
# ===========================================================================

class ReportedRAMModel(InvgateObject):
    """A class for storing reported RAM model data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, id: str, model_name: str, model: str, name: str, description: str, status: str, icon: str, kind: str, sku: str, is_manual: bool, import_uuid: str, updated_at: str, capacity: int, speed: int, device_type: str, width: int, manufacturer: ReportedManufacturer):
        """Creates a new ReportedRAMModel object.

        Args:
            id (str): The model's ID.
            model_name (str): The model's name name.
            model (str): The model's model.
            name (str): The model's name.
            description (str): The model's description.
            status (str): The model's status.
            icon (str): The model's icon.
            kind (str): The model's kind.
            sku (str): The model's SKU.
            is_manual (bool): Whether or not the model is manual.
            import_uuid (str): The model's import UUID.
            updated_at (str): When last the model was updated.
            capacity (int): The model's capacity.
            speed (int): The model's speed.
            device_type (str): The model's device type.
            width (int): The model's width.
            manufacturer (ReportedManufacturer): The model's manufacturer.
        """
        
        self.id: str = id
        self.model_name: str = model_name
        self.model: str = model
        self.name: str = name
        self.description: str = description
        self.status: str = status
        self.icon: str = icon
        self.kind: str = kind
        self.sku: str = sku
        self.is_manual: bool = is_manual
        self.import_uuid: str = import_uuid
        self.updated_at: str = updated_at
        self.capacity: int = capacity
        self.speed: int = speed
        self.device_type: str = device_type
        self.width: int = width
        self.manufacturer: ReportedManufacturer = manufacturer

class ReportedRAMModule(InvgateObject):
    """A class for storing reported RAM module data in memory. Inherits from the InvgateObject class.
    """

    def __init__(self, id: str, bank: str, capacity: int, speed: int, device_type: str, width: int, serial: str, created_at: str, deleted_at: str, model: ReportedRAMModel):
        """Creates a new ReportedRAMModule object.

        Args:
            id (str): The module's ID.
            bank (str): The module's bank.
            capacity (int): The module's capacity.
            speed (int): The module's speed.
            device_type (str): The module's device type.
            width (int): The module's width.
            serial (str): The module's serial.
            created_at (str): When the module was created.
            deleted_at (str): When the module was deleted.
            model (ReportedRAMModel): The module's model.
        """
        
        self.id: str = id
        self.bank: str = bank
        self.capacity: int = capacity
        self.speed: int = speed
        self.device_type: str = device_type
        self.width: int = width
        self.serial: str = serial
        self.created_at: str = created_at
        self.deleted_at: str = deleted_at
        self.model: ReportedRAMModel = model

# ===========================================================================
# Storage
# ===========================================================================

class ReportedStorageModel(InvgateObject):
    """A class for storing reported storage model data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, id: str, model_name: str, model: str, name: str, description: str, status: str, icon: str, kind: str, sku: str, is_manual: bool, import_uuid: str, updated_at: str, device_type: str, disk_type: str, manufacturer: ReportedManufacturer):
        """Creates a new ReportedStorageModel object.

        Args:
            id (str): The model's ID.
            model_name (str): The model's model name.
            model (str): The model's model.
            name (str): The model's name.
            description (str): The model's description.
            status (str): The model's status.
            icon (str): The model's icon.
            kind (str): The model's kind.
            sku (str): The model's SKU.
            is_manual (bool): Whether or not the model is manual.
            import_uuid (str): The model's import UUID.
            updated_at (str): When last the model was updated.
            device_type (str): The model's device type.
            disk_type (str): The model's disk type.
            manufacturer (ReportedManufacturer): The model's manufacturer.
        """
        self.id: str = id
        self.model_name: str = model_name
        self.model: str = model
        self.name: str = name
        self.description: str = description
        self.status: str = status
        self.icon: str = icon
        self.kind: str = kind
        self.sku: str = sku
        self.is_manual: bool = is_manual
        self.import_uuid: str = import_uuid
        self.updated_at: str = updated_at
        self.device_type: str = device_type
        self.disk_type: str = disk_type
        self.manufacturer: ReportedManufacturer = manufacturer

class ReportedStorage(InvgateObject):
    """A class for storing reported storage data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, id: str, created_at: str, deleted_at: str, capacity: int, label: str, available: int, model: ReportedStorageModel):
        """Creates a new ReportedStorage object.

        Args:
            id (str): The storage's ID.
            created_at (str): When the storage was created.
            deleted_at (str): When the storage was deleted.
            capacity (int): The storage's capacity.
            label (str): The storage's label.
            available (int): How much data is left on the storage.
            model (ReportedStorageModel): The storage's model.
        """
        
        self.id: str = id
        self.created_at: str = created_at
        self.deleted_at: str = deleted_at
        self.capacity: int = capacity
        self.label: str = label
        self.available: int = available
        self.model: ReportedStorageModel = model

# ===========================================================================
# Printer
# ===========================================================================

class ReportedPrinterModel(InvgateObject):
    """A class for storing reported printer model data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, id: str, model_name: str, model: str, name: str, description: str, status: str, icon: str, kind: str, sku: str, is_manual: bool, import_uuid: str, updated_at: str, manufacturer: ReportedManufacturer):
        """Creates a new InvgatePrinterModel object.

        Args:
            id (str): The model's ID.
            model_name (str): The model's model name.
            model (str): The model's model.
            name (str): The model's name.
            description (str): The model's description.
            status (str): The model's status.
            icon (str): The model's icon.
            kind (str): The model's kind.
            sku (str): The model's SKU.
            is_manual (bool): Whether or not the model is manual.
            import_uuid (str): The model's import UUID.
            updated_at (str): When last the model was updated.
            manufacturer (ReportedManufacturer): The model's manufacturer.
        """
        
        self.id: str = id
        self.model_name: str = model_name
        self.model: str = model
        self.name: str = name
        self.description: str = description
        self.status: str = status
        self.icon: str = icon
        self.kind: str = kind
        self.sku: str = sku
        self.is_manual: bool = is_manual
        self.import_uuid: str = import_uuid
        self.updated_at: str = updated_at
        self.manufacturer: ReportedManufacturer = manufacturer

class ReportedPrinter(InvgateObject):
    """A class for storing reported printer data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, id: str, created_at: str, deleted_at: str, model: ReportedPrinterModel):
        """Creates a new ReportedPrinter object.

        Args:
            id (str): The printer's ID.
            created_at (str): When the printer was created.
            deleted_at (str): When the printer was deleted.
            model (ReportedPrinterModel): The printer's model.
        """
        
        self.id: str = id
        self.created_at = created_at
        self.deleted_at = deleted_at
        self.model = model

# ===========================================================================
# Monitor
# ===========================================================================

class ReportedMonitorModel(InvgateObject):
    """A class for storing reported monitor model data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, id: str, model_name: str, model: str, height_measurement_unit: str, width_measurement_unit: str, diagonal_measurement_unit: str, name: str, description: str, status: str, icon: str, kind: str, sku: str, is_manual: bool, import_uuid: str, updated_at: str, height: float, width: float, ratio: str, diagonal: float, resolution: str, manufacturer: ReportedManufacturer):
        """Creates a new ReportedMonitorModel object.

        Args:
            id (str): The model's ID.
            model_name (str): The model's name.
            model (str): The model's model.
            height_measurement_unit (str): The model's height measurement unit.
            width_measurement_unit (str): The model's width measurement unit.
            diagonal_measurement_unit (str): The model's diagonal measurement unit.
            name (str): The model's name.
            description (str): The model's description
            status (str): The model's status.
            icon (str): The model's icon.
            kind (str): The model's kind.
            sku (str): The model's SKU.
            is_manual (bool): Whether or not the model is manual.
            import_uuid (str): The model's import UUID.
            updated_at (str): When last the model was updated.
            height (float): The model's height.
            width (float): The model's width.
            ratio (str): The model's ratio.
            diagonal (float): The model's diagonal span.
            resolution (str): The model's resolution.
            manufacturer (ReportedManufacturer): The model's manufacturer.
        """
        
        self.id: str = id
        self.model_name: str = model_name
        self.model: str = model
        self.height_measurement_unit: str = height_measurement_unit
        self.width_measurement_unit: str = width_measurement_unit
        self.diagonal_measurement_unit: str = diagonal_measurement_unit
        self.name: str = name
        self.description: str = description
        self.status: str = status
        self.icon: str = icon
        self.kind: str = kind
        self.sku: str = sku
        self.is_manual: bool = is_manual
        self.import_uuid: str = import_uuid
        self.updated_at: str = updated_at
        self.height: float = height
        self.width: float = width
        self.ratio: str = ratio
        self.diagonal: float = diagonal
        self.resolution: str = resolution
        self.manufacturer: ReportedManufacturer = manufacturer

class ReportedMonitor(InvgateObject):
    """A class for storing reported monitor data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, id: str, created_at: str, deleted_at: str, edid: str, serial: str, model: ReportedMonitorModel):
        """Creates a new ReportedMonitor object.

        Args:
            id (str): The monitor's ID.
            created_at (str): When the monitor was created.
            deleted_at (str): When the monitor was deleted.
            edid (str): The monitor's EDID.
            serial (str): The monitor's serial number.
            model (ReportedMonitorModel): The monitor's model.
        """
        
        self.id: str = id
        self.created_at: str = created_at
        self.deleted_at: str = deleted_at
        self.edid: str = edid
        self.serial: str = serial
        self.model: ReportedMonitorModel = model

# ===========================================================================
# BIOS
# ===========================================================================

class ReportedBIOS(InvgateObject):
    """A class for storing reported BIOS data in memory. Inherits from the InvgateObject class.
    """
    
    def __init__(self, id: str, date: str, version: str):
        """Creates a new ReportedBIOS object.

        Args:
            id (str): The BIOS's ID.
            date (str): The BIOS's date.
            version (str): The BIOS's version.
        """
        
        self.id: str = id
        self.date: str = date
        self.version: str = version

# ===========================================================================
# Computer
# ===========================================================================
  
class InvgateComputer(InvgateObject):
    """A class for storing data reported by the Invgate Agent. Applicable to assets of type computer only. Inherits from the InvgateObject class.
    """
    def __init__(self, id: str, asset: InvgateAsset, total_ram: int, format_type: str, name: str, inventory_id: str, serial: str, virtual: str, firewall_status: str, antivirus_status: str, connectivity_status: str, last_logged_user: str, osinfo: ReportedOSInfo, geolocation: ReportedGeolocation, motherboard: ReportedMotherboard, cpus: list[ReportedCPU], rams: list[ReportedRAMModule], storages: list[ReportedStorage], printers: list[ReportedPrinter], monitors: list[ReportedMonitor], bios: ReportedBIOS):
        """Creates a new InvgateComputer object.

        Args:
            id (str): The computer's ID.
            asset (InvgateAsset): The asset linking to the computer.
            total_ram (int): The computer's total installed RAM.
            format_type (str): The computer's format type.
            name (str): The computer's name.
            inventory_id (str): The computer's inventory ID.
            serial (str): The computer's serial number.
            virtual (str): The computer's virtual status.
            firewall_status (str): The computer's firewall status.
            antivirus_status (str): The computer's antivirus status.
            connectivity_status (str): The computer's connectivity status.
            last_logged_user (str): The computer's last logged user.
            osinfo (ReportedOSInfo): A set of info relating to the computer's OS.
            geolocation (ReportedGeolocation): The computer's geolocation.
            motherboard (ReportedMotherboard): The computer's motherboard.
            cpus (list[ReportedCPU]): A list of the computer's CPUs
            rams (list[ReportedRAM]): A list of the computer's RAM modules.
            storages (list[ReportedStorage]): A list of the computer's storages.
            printers (list[ReportedPrinter]): A list of the computer's printers.
            monitors (list[ReportedMonitor]): A list of the computer's monitors.
            bios (ReportedBIOS): The computer's BIOS.
        """
        
        self.id: str = id
        self.asset: InvgateAsset = asset
        self.total_ram: int = total_ram
        self.format_type: str = format_type
        self.name: str = name
        self.inventory_id: str = inventory_id
        self.serial: str = serial
        self.virtual: str = virtual
        self.firewall_status: str = firewall_status
        self.antivirus_status: str = antivirus_status
        self.connectivity_status: str = connectivity_status
        self.last_logged_user: str = last_logged_user
        self.osinfo: ReportedOSInfo = osinfo
        self.geolocation: ReportedGeolocation = geolocation
        self.motherboard: ReportedMotherboard = motherboard
        self.cpus: list[ReportedCPU] = cpus
        self.rams: list[ReportedRAMModule] = rams
        self.storages: list[ReportedStorage] = storages
        self.printers: list[ReportedPrinter] = printers
        self.monitors: list[ReportedMonitor] = monitors
        self.bios: ReportedBIOS = bios