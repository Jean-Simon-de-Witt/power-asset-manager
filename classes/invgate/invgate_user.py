class InvgateUser:
    def __init__(self, id = None, name = None, email = None, date_of_birth = None, employee_id = None, position = None, department = None, company = None, phone = None, cellphone = None, address = None, person_type = None, user = None, manager = None, location = None, cost_center = None):
        self.id = id
        self.name = name
        self.email = email
        self.date_of_birth = date_of_birth
        self.employee_id = employee_id
        self.position = position
        self.department = department
        self.company = company
        self.phone = phone
        self.cellphone = cellphone
        self.address = address
        self.person_type = person_type
        self.user = user
        self.manager = manager
        self.location = location
        self.cost_center = cost_center

    def to_string(self) -> str:
        if self.id and self.name:
            string = f"ID: {self.id}\nName: {self.name}\nEmail: {self.email}\nDate of Birth: {self.date_of_birth}\nEmployee ID: {self.employee_id}\nPosition: {self.position}\nDepartment: {self.department}\nCompany: {self.company}\nPhone: {self.phone}\nCellphone: {self.cellphone}\nAddress: {self.address}\nPerson Type: {self.person_type}\nUser: {self.user}\nManager: {self.manager}\nLocation: {self.location}\nCost Center: {self.cost_center}\n"
        else:
            string = "User not found."
        return string