class InvgatePurchaseOrder:
    def __init__(self, id, order_number, vendor = None, purchase_order_type = None, creation_date = None, expected_delivery_date = None, date_delivered = None, ship_method = None, ship_to = None, shipping_address = None, ship_instructions = None, billing_address = None, status = None, subtotal = None, freight = None, handling = None, tax = None, total_cost = None, cost_center = None, contract = None, requested_by = None, items = None):
        self.id = id
        self.order_number = order_number
        self.vendor = vendor
        self.purchase_order_type = purchase_order_type
        self.creation_date = creation_date
        self.expected_delivery_date = expected_delivery_date
        self.date_delivered = date_delivered
        self.ship_method = ship_method
        self.ship_to = ship_to
        self.shipping_address = shipping_address
        self.ship_instructions = ship_instructions
        self.billing_address = billing_address
        self.status = status
        self.subtotal = subtotal
        self.freight = freight
        self.handling = handling
        self.tax = tax
        self.total_cost = total_cost
        self.cost_center = cost_center
        self.contract = contract
        self.requested_by = requested_by
        self.items = items

    def to_string(self) -> str:
        return f"ID: {self.id}\nOrder Number: {self.order_number}\nVendor: {self.vendor}\nPurchase Order Type: {self.purchase_order_type}\nCreation Date: {self.creation_date}\nExpected Delivery Date: {self.expected_delivery_date}\nDate Delivered: {self.date_delivered}\nShip Method: {self.ship_method}\nShip To: {self.ship_to}\nShipping Address: {self.shipping_address}\nShip Instructions: {self.ship_instructions}\nBilling Address: {self.billing_address}\nStatus: {self.status}\nSubtotal: {self.subtotal}\nFreight: {self.freight}\nHandling: {self.handling}\nTax: {self.tax}\nTotal Cost: {self.total_cost}\nCost Center: {self.cost_center}\nContract: {self.contract}\nRequested By: {self.requested_by}\nItems: {self.items}\n"
