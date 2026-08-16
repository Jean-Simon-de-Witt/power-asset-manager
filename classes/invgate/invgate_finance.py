from classes.invgate.invgate_object import InvgateObject
from classes.invgate.invgate_vendor import InvgateVendor
from classes.invgate.invgate_purchase_order import InvgatePurchaseOrder

class InvgateFinance(InvgateObject):
    """
    A class for storing Invgate Finance objects in memory.
    """
    def __init__(self, id: int, asset: int, acquisition_type: str, acquisition_date: str, acquisition_price: float, actual_price: float, depreciation_percentage: float, residual_value: float, warranty_date: str, vendor: InvgateVendor, cost_center: str, purchase_order: InvgatePurchaseOrder, invoice_id: str):
        """Creates a new InvgateFinance object. Inherits from the InvgateObject class.

        Args:
            id (int): The finance's ID.
            asset (int): The ID of the asset the finance belongs to.
            acquisition_type (str): How the asset was acquired.
            acquisition_date (str): When the asset was acquired.
            acquisition_price (float): The asset's acquisition cost.
            actual_price (float): The asset's current cost.
            depreciation_percentage (float): The rate at which the asset's value depreciates.
            residual_value (float): The asset's scrap value.
            warranty_date (str): The date the asset's warranty expires.
            vendor (InvgateVendor): The asset's vendor.
            cost_center (str): The finance's cost center.
            purchase_order (InvgatePurchaseOrder): The asset's purchase order.
            invoice_id (str): The asset's invoice ID.
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
        self.vendor: InvgateVendor = vendor
        self.cost_center: str = cost_center
        self.purchase_order: InvgatePurchaseOrder = purchase_order
        self.invoice_id: str = invoice_id