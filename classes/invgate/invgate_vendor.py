from classes.invgate.invgate_object import InvgateObject

class InvgateVendor(InvgateObject):
    """
    A class for storing Invgate Vendor objects in memory. Inherits from the InvgateObject class.
    """
    def __init__(self, id: int, company_name: str, legal_name: str, status: str, tax_id: str, country: str, website: str, address: str, email: str, billing_currency: str, phone: str, industry: str):
        """Creates a new InvgateVendor object.

        Args:
            id (int): The vendor's ID.
            company_name (str): The vendor's company name.
            legal_name (str): The vendor's legal name.
            status (str): The vendor's status.
            tax_id (str): The vendor's tax ID.
            country (str): The vendor's country.
            website (str): The vendor's website.
            address (str): The vendor's address.
            email (str): The vendor's email.
            billing_currency (str): The vendor's billing currency.
            phone (str): The vendor's phone number.
            industry (str): The vendor's industry.
        """

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
