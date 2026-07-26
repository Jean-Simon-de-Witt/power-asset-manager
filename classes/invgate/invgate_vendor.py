class InvgateVendor:
    def __init__(self, id = None, company_name = None, legal_name = None, status = None, country = None, address = None, email = None, billing_currency = None, phone = None, industry = None):
        self.id = id
        self.company_name = company_name
        self.legal_name = legal_name
        self.status = status
        self.country = country
        self.address = address
        self.email = email
        self.billing_currency = billing_currency
        self.phone = phone
        self.industry = industry

    def to_string(self) -> str:
        if self.id and self.company_name:
            string = f"ID: {self.id}\nCompany Name: {self.company_name}\nLegal Name: {self.legal_name}\nStatus: {self.status}\nCountry: {self.country}\nAddress: {self.address}\nEmail: {self.email}\nBilling Currency: {self.billing_currency}\nPhone: {self.phone}\nIndustry: {self.industry}\n"
        else:
            string = "Vendor not found." 
        return string