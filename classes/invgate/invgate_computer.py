from classes.invgate.invgate_cpu import InvgateCPU
from classes.invgate.invgate_motherboard import InvgateMotherboard
from classes.invgate.invgate_ram import InvgateRAM
from classes.invgate.invgate_finance import InvgateFinance

class InvgateComputer:
    def __init__(self, id, total_storage, total_ram, format_type, name, inventory_id, serial, virtual, match_field, firewall_status, antivirus_status, status, connection_status, lifecycle_status, motherboard: InvgateMotherboard, cpu: InvgateCPU, ram: InvgateRAM, finance: InvgateFinance):
        self.id = id
        self.total_storage = total_storage
        self.total_ram = total_ram
        self.format_type = format_type
        self.name = name
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