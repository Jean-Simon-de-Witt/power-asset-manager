from classes.invgate.invgate_location import InvgateLocation
class InvgateUser:
    def __init__(self, id: int, name: str, email: str = None, date_of_birth: str = None, employee_id: str = None, position: str = None, department: str = None, company: str = None, phone: str = None, cellphone: str = None, address: str = None, person_type: str = None, user: str = None, manager: InvgateUser = None, location: InvgateLocation = None, cost_center = None):
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
        string = f"ID: {self.id}\n"
        string += f"Name: {self.name}\n"
        string += f"Email: {self.email}\n"
        string += f"Date of Birth: {self.date_of_birth}\n"
        string += f"Employee ID: {self.employee_id}\n"
        string += f"Position: {self.position}\n"
        string += f"Department: {self.department}\n"
        string += f"Company: {self.company}\n"
        string += f"Phone: {self.phone}\n"
        string += f"Cellphone: {self.cellphone}\n"
        string += f"Address: {self.address}\n"
        string += f"Person Type: {self.person_type}\n"
        string += f"User: {self.user}\n"

        if self.manager:
            string += "Manager:\n"
            string += f"\tID: {self.manager.id}\n"
            string += f"\tName: {self.manager.id}\n"
            string += f"\tEmail: {self.manager.email}\n"
            string += f"\tDate of Birth: {self.manager.date_of_birth}\n"
            string += f"\tEmployee ID: {self.manager.employee_id}\n"
            string += f"\tPosition: {self.manager.position}\n"
            string += f"\tDepartment: {self.manager.department}\n"
            string += f"\tCompany: {self.manager.company}\n"
            string += f"\tPhone: {self.manager.phone}\n"
            string += f"\tCellphone: {self.manager.cellphone}\n"
            string += f"\tAddress: {self.manager.address}\n"
            string += f"\tPerson Type: {self.manager.person_type}\n"
            string += f"\tUser: {self.manager.user}\n"
            string += f"\tCost Center: {self.manager.cost_center}\n"
        else:
            string += "Manager: None\n"

        if self.location:
            string += "Location:\n"
            string += f"\tID: {self.location.id}\n"
            string += f"\tName: {self.location.name}\n"
            string += f"\tFull Path: {self.location.full_path}\n"
            string += f"\tDescription: {self.location.description}\n"
        else:
            string += "Location: None\n"
        string += f"Cost Center: {self.cost_center}\n"
        return string