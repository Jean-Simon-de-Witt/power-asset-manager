from classes.invgate.invgate_vendor import InvgateVendor
from classes.invgate.invgate_purchase_order import InvgatePurchaseOrder
class InvgateFinance:
    def __init__(self, id: int, asset: int, acquisition_type: str = None, acquisition_date: str = None, acquisition_price: float = None, actual_price: float = None, residual_value: float = None, depreciation_percentage: str = None, warranty_date: str = None, vendor: InvgateVendor = None, cost_center: str = None, purchase_order: InvgatePurchaseOrder = None, invoice_id: str = None):
        self.id = id
        self.asset = asset
        self.acquisition_type = acquisition_type
        self.acquisition_date = acquisition_date
        self.acquisition_price = acquisition_price
        self.actual_price = actual_price
        self.residual_value = residual_value
        self.depreciation_percentage = depreciation_percentage
        self.warranty_date = warranty_date
        self.vendor = vendor # Stored in object as InvgateVendor object, but only vendor_id should be exported back to the endpoint.
        self.cost_center = cost_center
        self.purchase_order = purchase_order # Stored in object as InvgatePurchaseOrder object, but only order_id should be exported back to the endpoint.
        self.invoice_id = invoice_id

    def to_string(self) -> str:
        return f"ID: {self.id}\nAsset: {self.asset}\nAcquisition Type: {self.acquisition_type}\nAcquisition Date: {self.acquisition_date}\nAcquisition Price: {self.acquisition_price}\nActual Price: {self.actual_price}\nResidual Value: {self.residual_value}\nDepreciation Percentage: {self.depreciation_percentage}\nWarranty Date: {self.warranty_date}\nSupplier: {self.vendor}\nCost Center: {self.cost_center}\nOrder ID: {self.purchase_order}\nInvoice ID: {self.invoice_id}\n"
        