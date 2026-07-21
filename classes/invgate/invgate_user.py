class InvgateUser:
    def __init__(self, name, email ,id = None, email_display = None, date_of_birth = None, employee_id = None, position = None, department = None, company = None, phone = None, cellphone = None, address = None, person_type = None, is_deleted = None):
        self.id = id
        self.name = name
        self.email = email
        self.email_display = email_display
        self.date_of_birth = date_of_birth
        self.employee_id = employee_id
        self.position = position
        self.department = department
        self.company = company
        self.phone = phone
        self.cellphone = cellphone
        self.address = address
        self.person_type = person_type
        self.is_deleted = is_deleted

    def print(self):
        print(f"ID: {self.id}\nName: {self.name}\nEmail: {self.email}\nEmail Display: {self.email_display}\nDate of Birth: {self.data_of_birth}\nEmployee ID: {self.employee_id}\nPosition: {self.position}\nDepartment: {self.department}\nCompany: {self.company}\nPhone: {self.phone}\nCellphone: {self.cellphone}\nAddress: {self.address}\nPerson Type: {self.person_type}\n")

    def to_json(self, include_id=False):
        attributes = {
            "name": self.name,
            "email": self.email,
            "date_of_birth": self.date_of_birth,
            "employee_id": self.employee_id,
            "position": self.position,
            "department": self.department,
            "company": self.company,
            "phone": self.phone,
            "cellphone": self.cellphone,
            "address": self.address,
            "person_type": self.person_type
        }

        clean_attributes = {k: v for k, v in attributes.items() if v is not None}
        payload = {
            "data": {
                "type": "Person",
                "attributes": clean_attributes
            }
        }

        if include_id and self.id:
            payload["data"]["id"] = str(self.id)
        
        return payload