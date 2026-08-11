from classes.invgate.invgate_vendor import InvgateVendor
from classes.invgate.invgate_purchase_order import InvgatePurchaseOrder
class InvgateFinance:
    """
    A class for storing Invgate Finance objects in memory.
    """
    def __init__(self, id: int, asset: int, acquisition_type: str, acquisition_date: str, acquisition_price: float, actual_price: float, depreciation_percentage: float, residual_value: float, warranty_date: str, vendor: InvgateVendor, cost_center: str, purchase_order: InvgatePurchaseOrder, invoice_id: str):
        """
        Creates a new InvgateFinance object.

        Arguments:
            asset* (int): The unique identifier linking to the asset's ID.
            id (int): The unique identifier for each finance object.
            acquisition_type (str): How the asset was acquired.
            acquisition_date (str): The date of the acquisition.
            acquisition_price (float): The price of the acquisition.
            actual_price (float): The current price of the asset.
            residual_value (float): The residual or scrap value of the asset.
            depreciation_percentage (str): The percentage of value depreciation undergone by the asset.
            warranty_date (str): The warranty's expiration date.
            vendor (InvgateVendor): The asset's vendor.
            cost_center (str): The asset's cost center.
            purchase_order (InvgatePurchaseOrder): The asset's purchase order.
            invoice_id (str): The asset's invoice ID.

        Returns:
            None:
        """
        self.id: int = id
        self.asset: int = asset
        self.acquisition_type: str = acquisition_type
        self.acquisition_date: str = acquisition_date
        self.acquisition_price: float = acquisition_price
        self.actual_price: float = actual_price
        self.depreciation_percentage: float = depreciation_percentage
        self.residual_value: float = residual_value
        self.warranty_date: str = warranty_date
        self.vendor: InvgateVendor = vendor # Stored in object as InvgateVendor object, but only vendor_id should be exported back to the endpoint.
        self.cost_center: str = cost_center
        self.purchase_order: InvgatePurchaseOrder = purchase_order # Stored in object as InvgatePurchaseOrder object, but only order_id should be exported back to the endpoint.
        self.invoice_id: str = invoice_id

    def to_string(self) -> str:
        """
        Exports the object's properties as a formatted string.

        Arguments:
            None:

        Returns:
            string (str): The object's properties as a formatted string.
        """
        string = f"ID: {self.id}\n"
        string += f"Asset ID: {self.asset}\n"
        string += f"Acquisition Type: {self.acquisition_type}\n"
        string += f"Acquisition Date: {self.acquisition_date}\n"
        string += f"Acquisition Price: {self.acquisition_price}\n"
        string += f"Actual Price: {self.actual_price}\n"
        string += f"Residual Value: {self.residual_value}\n"
        string += f"Depreciation Percentage: {self.depreciation_percentage}\n"
        string += f"Warranty Date: {self.warranty_date}\n"

        if self.vendor:
            string += "Vendor: \n"
            string += f"\tID: {self.vendor.id}\n"
            string += f"\tCompany Name: {self.vendor.company_name}\n"
            string += f"\tLegal Name: {self.vendor.legal_name}\n"
            string += f"\tStatus: {self.vendor.status}\n"
            string += f"\tCountry: {self.vendor.country}\n"
            string += f"\tAddress: {self.vendor.address}\n"
            string += f"\tEmail: {self.vendor.email}\n"
            string += f"\tBilling Currency: {self.vendor.billing_currency}\n"
            string += f"\tPhone: {self.vendor.phone}\n"
            string += f"\tIndustry: {self.vendor.industry}\n"
        else:
            string += "Vendor: None\n"
        string += f"Cost Center: {self.cost_center}\n"

        if self.purchase_order:
            string += f"Purchase Order:\n"
            string += f"\tID: {self.purchase_order.id}\n"
            string += f"\tOrder Number: {self.purchase_order.order_number}\n"
            string += f"\tPurchase Order Type: {self.purchase_order.purchase_order_type}\n"
            string += f"\tCreation Date: {self.purchase_order.creation_date}\n"
            string += f"\tExpected Delivery Date: {self.purchase_order.expected_delivery_date}\n"
            string += f"\tDate Delivered: {self.purchase_order.date_delivered}\n"
            string += f"\tShip Method: {self.purchase_order.ship_method}\n"
            string += f"\tShip To: {self.purchase_order.ship_to}\n"
            string += f"\tShipping Address: {self.purchase_order.shipping_address}\n"
            string += f"\tShip Instructions: {self.purchase_order.ship_instructions}\n"
            string += f"\tBilling Address: {self.purchase_order.billing_address}\n"
            string += f"\tStatus: {self.purchase_order.status}\n"
            string += f"\tSubtotal: {self.purchase_order.subtotal}\n"
            string += f"\tFreight: {self.purchase_order.freight}\n"
            string += f"\tHandling: {self.purchase_order.handling}\n"
            string += f"\tTax: {self.purchase_order.tax}\n"
            string += f"\tTotal Cost: {self.purchase_order.total_cost}\n"
            string += f"\tCost Center: {self.purchase_order.cost_center}\n"
            string += f"\tContract: {self.purchase_order.contract}\n"
            string += f"\tRequested By: {self.purchase_order.requested_by}\n"
            string += f"\tItems: {self.purchase_order.items}\n"
        else:
            string += "Purchase Order: None\n"
        string += f"Invoice ID: {self.invoice_id}\n"
        return string