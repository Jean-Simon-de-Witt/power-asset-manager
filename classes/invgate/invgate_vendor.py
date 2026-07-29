class InvgateVendor:
    def __init__(self, id: int, company_name: str, legal_name: str = None, status: str = None, country: str = None, address: str = None, email: str = None, billing_currency: str = None, phone: str = None, industry: str = None):
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