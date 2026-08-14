from classes.invgate.invgate_object import InvgateObject
from classes.invgate.invgate_vendor import InvgateVendor

class InvgatePurchaseOrder(InvgateObject):
    """
    A class for storing Invgate Purchase Order objects in memory.
    """
    def __init__(self, id: int, order_number: str, vendor: InvgateVendor, purchase_order_type: str, creation_date: str, expected_delivery_date: str, date_delivered: str, ship_method: str, billing_address: str, status: str, subtotal: float, freight: str, handling: str, tax: float, total_cost: float, cost_center: str, contract: str):

        self.id: int = id
        self.order_number: str = order_number
        self.vendor: InvgateVendor = vendor
        self.purchase_order_type: str = purchase_order_type
        self.creation_date: str = creation_date
        self.expected_delivery_date: str = expected_delivery_date
        self.date_delivered: str = date_delivered
        self.ship_method: str = ship_method
        self.billing_address: str = billing_address
        self.status: str = status
        self.subtotal: float = subtotal
        self.freight: str = freight
        self.handling: str = handling
        self.tax: float = tax
        self.total_cost: float = total_cost
        self.cost_center: str = cost_center
        self.contract: str = contract