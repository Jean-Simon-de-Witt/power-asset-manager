class InvgateFinance:
    def __init__(self, id, asset, acquisition_type, acquisition_date, acquisition_price, actual_price, depreciation_percentage, residual_value, warranty_date, supplier, cost_center, order_id, invoice_id):
        self.id = id
        self.asset = asset
        self.acquisition_type = acquisition_type
        self.acquisition_date = acquisition_date
        self.acquisition_price = acquisition_price
        self.actual_price = actual_price
        self.depreciation_percentage = depreciation_percentage
        self.residual_value = residual_value
        self.warranty_date = warranty_date
        self.supplier = supplier
        self.cost_center = cost_center
        self.order_id = order_id
        self.invoice_id = invoice_id