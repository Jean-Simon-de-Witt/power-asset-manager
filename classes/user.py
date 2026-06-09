from invgate_connection import InvgateConnection as connection
from invgate_routes import InvgateRoutes as routes

class User:
    def __init__(self, name, email, email_display, date_of_birth, person_id, position, department, company, phone, cellphone, address, person_type, is_deleted):
        self.name = name
        self.email = email
        self.email_display = email_display
        self.data_of_birth = date_of_birth
        person_id = person_id
        self.position = position
        self.department = department
        self.company = company
        self.phone = phone
        self.cellphone = cellphone
        self.address = address
        self.person_type = person_type
        self.is_deleted = is_deleted