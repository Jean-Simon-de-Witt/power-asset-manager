from classes.invgate.invgate_cpu import InvgateCPU
from classes.invgate.invgate_motherboard import InvgateMotherboard
from classes.invgate.invgate_ram import InvgateRAM
from classes.invgate.invgate_finance import InvgateFinance

class InvgateComputer:
    def __init__(self, id, total_storage, total_ram, format_type, name, inventory_id, serial, virtual, match_field, firewall_status, antivirus_status, status, connection_status, lifecycle_status, mac_address, motherboard: InvgateMotherboard, cpu: InvgateCPU, ram: InvgateRAM, finance: InvgateFinance):
        self.id = id
        self.total_storage = total_storage
        self.total_ram = total_ram
        self.format_type = format_type
        self.name = name
        self.mac_address = mac_address
        self.inventory_id = inventory_id
        self.serial = serial
        self.virtual = virtual
        self.match_field = match_field
        self.firewall_status = firewall_status
        self.antivirus_status = antivirus_status
        self.status = status
        self.connection_status = connection_status
        self.lifecycle_status = lifecycle_status
        self.motherboard = motherboard
        self.cpu = cpu
        self.ram = ram
        self.finance = finance

    def print(self):
        print(f"ID: {self.id}\nTotal Storage: {self.total_storage}\nTotal RAM: {self.total_ram}\nFormat Type: {self.format_type}\nName: {self.name}\nInventory ID: {self.inventory_id}\nSerial: {self.serial}\nVirtual: {self.virtual}\nMatch Field: {self.match_field}\nFirewall Status: {self.firewall_status}\nAntivirus Status: {self.antivirus_status}\nStatus: {self.status}\nConnection Status: {self.connection_status}\nLifecycle Status: {self.lifecycle_status}\nWi-Fi MAC Address: {self.mac_address}\nMotherboard ID: {self.motherboard.id}\nMotherboard Model: {self.motherboard.model}\nMotherboard Manufacturer ID: {self.motherboard.manufacturer_id}\nMotherboard Manufacturer Name: {self.motherboard.manufacturer_name}\nMotherboard Manufacturer Support URL: {self.motherboard.manufacturer_support_url}\nMotherboard Manufacturer Website URL: {self.motherboard.manufacturer_website_url}\nCPU ID: {self.cpu.id}\nCPU Model Name: {self.cpu.model_name}\nCPU Model: {self.cpu.model}\nCPU Kind: {self.cpu.kind}\nImport UUID: {self.cpu.import_uuid}\nUpdated At: {self.cpu.updated_at}\nCPU Family: {self.cpu.family}\nCPU Frequency: {self.cpu.frequency}\nCPU Cores: {self.cpu.cores}\nCPU Manufacturer ID: {self.cpu.manufacturer_id}\nCPU Manufacturer Name: {self.cpu.manufacturer_name}\nCPU Manufacturer Support URL: {self.cpu.manufacturer_support_url}\nCPU Manufacturer Website URL: {self.cpu.manufacturer_website_url}\nRAM ID: {self.ram.id}\nRAM Model Name: {self.ram.model_name}\nRAM Model: {self.ram.model}\nRAM Kind: {self.ram.kind}\nRAM Capacity: {self.ram.capacity}\nRAM Speed: {self.ram.speed}\nRAM Device Type: {self.ram.device_type}\nRAM Width: {self.ram.width}\nRAM Manufacturer ID: {self.ram.manufacturer_id}\nRAM Manufacturer Name: {self.ram.manufacturer_name}\nRAM Manufacturer Support URL: {self.ram.manufacturer_support_url}\nRAM Manufacturer Website URL: {self.ram.manufacturer_website_url}\nFinance ID: {self.finance.id}\nFinance Asset: {self.finance.asset}\nFinance Acquisition Type: {self.finance.acquisition_type}\nFinance Acquisition Date: {self.finance.acquisition_date}\nFinance Acquisition Price: {self.finance.acquisition_price}\nFinance Actual Price: {self.finance.actual_price}\nFinance Depreciation Percentage: {self.finance.depreciation_percentage}\nFinance Residual Value: {self.finance.residual_value}\nFinance Warranty Date: {self.finance.warranty_date}\nFinance Supplier: {self.finance.supplier}\nFinance Cost Center: {self.finance.cost_center}\nFinance Order ID: {self.finance.order_id}\nFinance Invoice ID: {self.finance.invoice_id}\n")