from classes.invgate.invgate_vendor import InvgateVendor
class InvgatePurchaseOrder:
    """
    A class for storing Invgate Purchase Order objects in memory.
    """
    def __init__(self, id: int, order_number: str, vendor: InvgateVendor, purchase_order_type: str, creation_date: str, expected_delivery_date: str, date_delivered: str, ship_method: str, billing_address: str, status: str, subtotal: float, freight: str, handling: str, tax: float, total_cost: float, cost_center: str, contract: str):
        """
        Creates a new InvgatePurchaseOrder object.
        
        Arguments:
            order_number* (str): The purchase order's number.
            id (int): The unique identifier for each purchase order object.
            vendor (InvgateVendor): The purchase order's vendor.
            purchase_order_type (str): The purchase order's type.
            creation_date (str): The purchase order's creation date.
            expected_delivery_date (str): The purchase order's expected delivery date.
            date_delivered (str): The date of the purchase order's delivery.
            ship_method (str): The purchase order's ship method.
            ship_to (str): Where the purchase order is to be shipped.
            shipping_address (str): The purchase order's shipping address.
            ship_instructions (str): The purchase order's shipping instructions.
            billing_address (str): Where the purchase order is billed to.
            status (str): The purchase order's status.
            subtotal (float): The purchase order's subtotal.
            freight (str): The purchase order's freight.
            handling (str): How the purchase order is to be handled.
            tax (float): The purchase order's tax.
            total_cost (float): The purchase order's total cost.
            cost_center (str): The purchase order's cost center.
            contract (str): The purchase order's contract.
            requested_by (str): The person that requested the purchase order.
            self.items (str): The list of items for the purchase order.

        Returns:
            None:
        """
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
        """
        Exports the object's properties as a formatted string.
        
        Arguments:
            None:

        Returns:
            string (str): The object's properties as a formatted string.
        """
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