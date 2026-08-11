from classes.invgate.invgate_location import InvgateLocation
class InvgateUser:
    """
    A class for storing Invgate User objects in memory.
    """
    def __init__(self, id: int, name: str, email: str, date_of_birth: str, employee_id: str, position: str, department: str, company: str, phone: str, cellphone: str, address: str, person_type: str, user_id: int, username: str, manager_id: int, manager_name: str, manager_email: str, location: InvgateLocation, cost_center: str):
        """
        Creates a new InvgateUser object.
        
        Arguments:
            id (int): The unique identifier for each user object.
            name* (str): The user's name.
            email (str): The user's email.
            date_of_birth (str): The user's date of birth.
            employee_id (str): The user's employee ID.
            position (str): The user's position.
            department (str): The user's department.
            company (str): The user's company.
            phone (str): The user's phone number.
            cellphone (str): The user's cellphone number.
            address (str): The user's address.
            person_type (str): The user's type.
            user (str): Unused.
            manager (InvgateUser): The user's manager.
            location (InvgateLocation): The user's location.
            cost_center (str): The user's cost center.

        Returns:
            None:
        """
        self.id: int = id
        self.name: str = name
        self.email: str = email
        self.date_of_birth: str = date_of_birth
        self.employee_id: str = employee_id
        self.position: str = position
        self.department: str = department
        self.company: str = company
        self.phone: str = phone
        self.cellphone: str = cellphone
        self.address: str = address
        self.person_type: str = person_type
        self.user_id: int = user_id
        self.username: str = username
        self.manager_id: int = manager_id
        self.manager_name: str = manager_name
        self.manager_email: str = manager_email
        self.location: InvgateLocation = location
        self.cost_center: str = cost_center

        self.matched_by: str = None

    def to_string(self) -> str:
        """
        Exports the object's properties as a formatted string.
        
        Arguments:
            None:

        Returns:
            string (str): The object's properties as a formatted string.
        """
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

        if self.manager_id:
            string += "Manager:\n"
            string += f"\tID: {self.manager_id}\n"
            string += f"\tName: {self.manager_name}\n"
            string += f"\tEmail: {self.manager_email}\n"
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

    def to_json(self, include_id: bool = False) -> dict:
        """
        Exports the object's properties as a JSON object.
        
        Arguments:
            include_id (bool): Whether or not to include the object's ID in the JSON object. Defaults to False.

        Returns:
            json (dict): The object's properties as a JSON object.
        """
        json = {}

        if self.id and include_id:
            json["id"] = self.id

        if self.name:
            json["name"] = self.name

        if self.email:
            json["email"] = self.email


        if self.date_of_birth:
            json["date_of_birth"] = self.date_of_birth

        if self.employee_id:
            json["employee_id"] = self.employee_id

        if self.position:
            json["position"] = self.position

        if self.department:
            json["department"] = self.department

        if self.company:
            json["company"] = self.company

        if self.phone:
            json["phone"] = self.phone

        if self.cellphone:
            json["cellphone"] = self.cellphone

        if self.address:
            json["address"] = self.address

        if self.person_type:
            json["person_type"] = self.person_type

        if self.user:
            json["user"] = self.user

        if self.manager_id:
            json["manager"] = self.manager_id

        if self.location:
            json["location"] = self.location.id

        if self.cost_center:
            json["cost_center"] = self.cost_center

        return json