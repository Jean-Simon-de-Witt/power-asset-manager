class InvgateUser:
    def __init__(self, name, email, email_display, date_of_birth, employee_id, position, department, company, phone, cellphone, address, person_type, is_deleted):
        self.name = name
        self.email = email
        self.email_display = email_display
        self.data_of_birth = date_of_birth
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
        print(f"Name: {self.name}\nEmail: {self.email}\nEmail Display: {self.email_display}\nDate of Birth: {self.data_of_birth}\nEmployee ID: {self.employee_id}\nPosition: {self.position}\nDepartment: {self.department}\nCompany: {self.company}\nPhone: {self.phone}\nCellphone: {self.cellphone}\nAddress: {self.address}\nPerson Type: {self.person_type}\n")