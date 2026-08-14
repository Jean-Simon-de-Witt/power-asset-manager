from classes.invgate.invgate_object import InvgateObject

class InvgateVendor(InvgateObject):
    """
    A class for storing Invgate Vendor objects in memory.
    """
    def __init__(self, id: int, company_name: str, legal_name: str, status: str, tax_id: str, country: str, website: str, address: str, email: str, billing_currency: str, phone: str, industry: str):

        self.id: int = id
        self.company_name: str = company_name
        self.legal_name: str = legal_name
        self.status: str = status
        self.tax_id: str = tax_id
        self.country: str = country
        self.website: str = website
        self.address: str = address
        self.email: str = email
        self.billing_currency: str = billing_currency
        self.phone: str = phone
        self.industry: str = industry
