from classes.invgate.invgate_vendor import InvgateVendor
class InvgatePurchaseOrder:
    def __init__(self, id: int, order_number: str, vendor: InvgateVendor = None, purchase_order_type: str = None, creation_date: str = None, expected_delivery_date: str = None, date_delivered: str = None, ship_method: str = None, ship_to: str = None, shipping_address: str = None, ship_instructions: str = None, billing_address: str = None, status: str = None, subtotal: float = None, freight: str = None, handling: str = None, tax: float = None, total_cost: float = None, cost_center: str = None, contract: str = None, requested_by: str = None, items: str = None):
        self.id: int = id
        self.order_number: str = order_number
        self.vendor: InvgateVendor = vendor
        self.purchase_order_type: str = purchase_order_type
        self.creation_date: str = creation_date
        self.expected_delivery_date: str = expected_delivery_date
        self.date_delivered: str = date_delivered
        self.ship_method: str = ship_method
        self.ship_to: str = ship_to
        self.shipping_address: str = shipping_address
        self.ship_instructions: str = ship_instructions
        self.billing_address: str = billing_address
        self.status: str = status
        self.subtotal: float = subtotal
        self.freight: str = freight
        self.handling: str = handling
        self.tax: float = tax
        self.total_cost: float = total_cost
        self.cost_center: str = cost_center
        self.contract: str = contract
        self.requested_by: str = requested_by
        self.items: str = items

    def to_string(self) -> str:
        string = f"ID: {self.id}\n"
        string += f"Order Number: {self.order_number}\n"

        if self.vendor:
            string += "Vendor:\n"
            string += f"\tID: {self.vendor.id}\n"
            string += f"\tCompany Name: {self.vendor.company_name}\n"
            string += f"\tLegal Name: {self.vendor.legal_name}\n"
            string += f"\tStatus: {self.vendor.status}\n"
            string += f"\tCountry: {self.vendor.country}\n"
            string += f"\tAddress: {self.vendor.address}\n"
            string += f"\tEmail: {self.vendor.email}\n"
            string += f"\tBilling Currency: {self.vendor.billing_currency}\n"
            string += f"\tPhone: {self.vendor.phone}"
            string += f"\tIndustry: {self.vendor.industry}\n"
        else:
            string += "Vendor: None\n"

        string += f"Purchase Order Type: {self.purchase_order_type}\n"
        string += f"Creation Date: {self.creation_date}\n"
        string += f"Expected Delivery Date: {self.expected_delivery_date}\n"
        string += f"Date Delivered: {self.date_delivered}\n"
        string += f"Ship Method: {self.ship_method}\n"
        string += f"Ship To: {self.ship_to}\n"
        string += f"Shipping Address: {self.shipping_address}\n"
        string += f"Ship Instructions: {self.ship_instructions}\n"
        string += f"Billing Address: {self.billing_address}\n"
        string += f"Status: {self.status}\n"
        string += f"Subtotal: {self.subtotal}\n"
        string += f"Freight: {self.freight}\n"
        string += f"Handling: {self.handling}\n"
        string += f"Tax: {self.tax}\n"
        string += f"Total Cost: {self.total_cost}\n"
        string += f"Cost Center: {self.cost_center}\n"
        string += f"Contract: {self.contract}\n"
        string += f"Requested By: {self.requested_by}\n"
        string += f"Items: {self.items}\n"
        return string