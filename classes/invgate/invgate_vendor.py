class InvgateVendor:
    """
    A class for storing Invgate Vendor objects in memory.
    """
    def __init__(self, id: int, company_name: str, legal_name: str, status: str, country: str, website: str, address: str, email: str, billing_currency: str, phone: str, industry: str):
        """
        Creates a new InvgateVendor object.
        
        Arguments:
            id* (int): The unique identifier for each vendor object.
            company_name* (str): The vendor's company name.
            legal_name (str): The vendor's legal name.
            status (str): The vendor's status.
            country (str): The vendor's country.
            address (str): The vendor's address.
            email (str): The vendor's email.
            billing_currency (str): The currency in which the vendor bills.
            phone (str): The vendor's phone number.
            industry (str): The industry in which the vendor operates.

        Returns:
            None:
        """
        self.id: int = id
        self.company_name: str = company_name
        self.legal_name: str = legal_name
        self.status: str = status
        self.country: str = country
        self.address: str = address
        self.email: str = email
        self.billing_currency: str = billing_currency
        self.phone: str = phone
        self.industry: str = industry

    def to_string(self) -> str:
        """
        Exports the object's properties as a formatted string.
        
        Arguments:
            None:
        
        Returns:
            string (str): The object's properties as a formatted string.
        """
        string = f"ID: {self.id}\n"
        string += f"Company Name: {self.company_name}\n"
        string += f"Legal Name: {self.legal_name}\n"
        string += f"Status: {self.status}\n"
        string += f"Country: {self.country}\n"
        string += f"Address: {self.address}\n"
        string += f"Email: {self.email}\n"
        string += f"Billing Currency: {self.billing_currency}\n"
        string += f"Phone: {self.phone}\n"
        string += f"Industry: {self.industry}\n"
        return string