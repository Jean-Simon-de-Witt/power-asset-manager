class InvgateFinance:
    def __init__(self, id, asset, acquisition_type = None, acquisition_date = None, acquisition_price = None, actual_price = None, residual_value = None, depreciation_percentage = None, warranty_date = None, supplier = None, cost_center = None, order_id = None, invoice_id = None):
        self.id = id
        self.asset = asset
        self.acquisition_type = acquisition_type
        self.acquisition_date = acquisition_date
        self.acquisition_price = acquisition_price
        self.actual_price = actual_price
        self.residual_value = residual_value
        self.depreciation_percentage = depreciation_percentage
        self.warranty_date = warranty_date
        self.supplier = supplier
        self.cost_center = cost_center
        self.order_id = order_id
        self.invoice_id = invoice_id

    def to_string(self) -> str:
        return f"ID: {self.id}\nAsset: {self.asset}\nAcquisition Type: {self.acquisition_type}\nAcquisition Date: {self.acquisition_date}\nAcquisition Price: {self.acquisition_price}\nActual Price: {self.actual_price}\nResidual Value: {self.residual_value}\nDepreciation Percentage: {self.depreciation_percentage}\nWarranty Date: {self.warranty_date}\nSupplier: {self.supplier}\nCost Center: {self.cost_center}\nOrder ID: {self.order_id}\nInvoice ID: {self.invoice_id}\n"
        