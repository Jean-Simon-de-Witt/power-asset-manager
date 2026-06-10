import requests
from classes.invgate.invgate_routes import InvgateRoutes as routes
from classes.invgate.invgate_user import InvgateUser
from classes.invgate.invgate_computer import InvgateComputer
from classes.invgate.invgate_cpu import InvgateCPU
from classes.invgate.invgate_motherboard import InvgateMotherboard
from classes.invgate.invgate_ram import InvgateRAM
from classes.invgate.invgate_finance import InvgateFinance

class InvgateConnection:
    # ==============================================================================================
    # Init function: Initializes the connection and attempts to authenticate
    # ==============================================================================================
    def __init__(self, domain, client_id, client_secret):
        # Initialise variables
        self.domain = domain.rstrip('/')
        self.client_id = client_id
        self.client_secret = client_secret

        # Initialise a session
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.access_token = None

        # Attempt to authenticate
        self.authenticate()
    # ==============================================================================================
    # Authenticate function: Attempts to authenticate, returns a token if successful.
    # ==============================================================================================
    def authenticate(self):
        auth_url = f"{self.domain}/oauth2/token/"

        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        try:
            # Send POST request to get token
            response = requests.post(auth_url, data=payload)
            response.raise_for_status() # Raises an error if HTTP request fails

            # Parse JSON response and extract token
            self.access_token = response.json().get("access_token")
            self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})

            print("InvGate connection and authorization successful.")
        except requests.exceptions.RequestException as e:
            # Handle error if connection unsuccessful
            print(f"Authentication failed. Please check credentials or URL.\nError: {e}")
            self.access_token = None

    # ==============================================================================================
    # Get Data function: Makes GET requests to the API using the authenticated session.
    # ==============================================================================================
    def get_data(self, endpoint_path):
        # Ends if not authenticated
        if not self.access_token:
            print("Unable to make request: Not authenticated")
            return None
        
        # Ensure endpoint starts with a slash
        if not endpoint_path.startswith('/'):
            endpoint_path = '/' + endpoint_path

        full_url = f"{self.domain}{endpoint_path}"

        try:
            # 1. Make the FIRST request exactly as provided (no page numbers added)
            response = self.session.get(full_url)
            response.raise_for_status()
            response_json = response.json()

            # 2. Check how InvGate formatted the response
            list_key = 'data' if 'data' in response_json else 'results'

            # 3. If it is a list of items, handle pagination
            if list_key in response_json and isinstance(response_json[list_key], list):
                all_data = []
                all_data.extend(response_json[list_key]) # Save the first page

                next_url = self.get_next_url(response_json)
                
                # Loop through remaining pages if a "next" key exists
                while next_url:
                    if not next_url.startswith('http'):
                        next_url = f"{self.domain}{next_url}"

                    response = self.session.get(next_url)
                    response.raise_for_status()
                    response_json = response.json()
                    
                    all_data.extend(response_json[list_key])

                    next_url = self.get_next_url(response_json)
                    
                return all_data
            
            # 4. ELSE it is a single record (like User 888). Return it immediately!
            else:
                return response_json
                
        except requests.exceptions.RequestException as e:
            print(f"GET request failed for {endpoint_path}: {e}")
            return None
    # ==============================================================================================
    # Post Data function: Creates and adds new records to the system using the authenticated session
    # ==============================================================================================
    def post_data(self, endpoint_path, payload):
        # End if not authenticated
        if not self.access_token:
            print("Unable to make request: Not authenticated")
            return None
        
        # Ensure endpoint starts with a slash
        if not endpoint_path.startswith('/'):
            endpoint_path = '/' + endpoint_path

        full_url = f"{self.domain}{endpoint_path}"

        try:
            # Requests library automatically formats data correctly for JSON payload when using json=payload
            response = self.session.post(full_url, json=payload)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"POST request failed for {endpoint_path}: {e}")

            if hasattr(e, 'response') and e.response is not None:
                print(f"Server response: {e.response.text}")
                return None

    # ==============================================================================================
    # Put Data function: Updates existing records in the system using the authenticated session
    # ==============================================================================================       
    def put_data(self, endpoint_path, payload):
        # End if not authenticated
        if not self.access_token:
            return None
        
        if not endpoint_path.startswith('/'):
            endpoint_path = '/' + endpoint_path

        full_url = f"{self.domain}{endpoint_path}"

        try:
            response = self.session.put(full_url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"PUT request failed for {endpoint_path}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Server response: {e.response.text}")
                return None
    
    # ==============================================================================================
    # Delete Data function: Deletes records from the system using the authenticated session
    # ==============================================================================================
    def delete_data(self, endpoint_path):
        if not self.access_token:
            return None
        
        if not endpoint_path.startswith('/'):
            endpoint_path = '/' + endpoint_path

        full_url = f"{self.domain}{endpoint_path}"

        try:
            response = self.session.delete(full_url)

            if response.text:
                return response.json()
            else:
                return {"status": "success", "message": "Record deleted successfully"}
        except requests.exceptions.RequestException as e:
            print(f"DELETE request failed for {endpoint_path}: {e}")
            return None

    # =========================================================================================================
    # Specific API endpoint functions: These use the generic get/post/put/delete functions with specific routes
    # =========================================================================================================

    def get_users(self):
        return self.get_data(routes.users())
    
    def get_user(self, id):
        return self.get_data(routes.user(id))
    
    def get_computers(self):
        return self.get_data(routes.computers_all_attributes())

    def get_computer(self, id):
        return self.get_data(routes.computer_all_attributes(id))
    
    def get_locations(self):
        return self.get_data(routes.locations())
    
    def get_finances(self):
        return self.get_data(routes.financials())
    
    def get_finance(self, id):
        return self.get_data(routes.financial(id))
        
    # ==========================================================================================================
    # Populate functions: These get data from the API and convert it into class instances stored in this class
    # ==========================================================================================================

    # Runs all populate functions
    def populate(self):
        self.populate_users()

    # Gets all users and stores them as classes in memory
    def populate_users(self):
        self.users = []
        user_data = self.get_users()

        for u in user_data:
            a = u.get("attributes")
            user = InvgateUser(a["name"], a["email"], a["email_display"], a["date_of_birth"], a["person_id"], a["position"], a["department"], a["company"], a["phone"], a["cellphone"], a["address"], a["person_type"], a["is_deleted"])
            self.users.append(user)

    def populate_computers(self):
        self.computers= []
        extracted_data = self.get_computers()
        computer_data = extracted_data.get("data", [])
        included_data = extracted_data.get("included", [])

        included_lookup = {}
        for item in included_data:
            item_type = item.get("type")
            item_id = item.get("id")

            if item_type not in included_lookup:
                included_lookup[item_type] = {}
            included_lookup[item_type][item_id] = item

        for c in computer_data:
            c.get("relationships", {})
            a = c.get("attributes", {})
            r = c.get("relationships", {})
            reported_cpu = r.get("reported_cpus", {}).get("data")
            cpu = included_lookup[reported_cpu.get("type")][reported_cpu.get("id")]


            reported_motherboard = r.get("reported_motherboard", {}).get("data")
            mb = included_lookup[reported_motherboard.get("type")][reported_motherboard.get("id")]

            reported_rams = r.get("reported_rams", {}).get("data")
            ram = included_lookup[reported_rams.get("type")][reported_rams.get("id")]

            finance_id = r.get("finance", {}).get("id")

            f = self.get_finance(finance_id)
            computer = InvgateComputer(c["id"],c["total_storage"], c["total_ram"], c["format_type"], c["name"], c["inventory_id"], c["serial"], c["virtual"], c["match_field"], c["firewall_status"], c["status"], c["antivirus_status"], c["connection_status"], c["lifecycle_status"], InvgateMotherboard(mb["id"], mb["model"], mb["manufacturer_name"],mb["manufacturer_id"],mb["manufacturer_support_url"], mb["manufacturer_website_url"]), InvgateCPU(cpu["id"], cpu["model_name"], cpu["model"], cpu["kind"], cpu["import_uuid"], cpu["updated_at"], cpu["family"], cpu["frequency"], cpu["cores"], cpu["manufacturer_id"], cpu["manufacturer_name"], cpu["manufacturer_support_url"], cpu["manufacturer_website_url"]), InvgateRAM(ram["id"], ram["model_name"], ram["model"], ram["kind"], ram["import_uuid"], ram["updated_at"], ram["capacity"], ram["speed"], ram["device_type"], ram["width"], ram["manufacturer_id"], ram["manufacturer_name"], ram["manufacturer_support_url"], ram["manufacturer_website_url"]), InvgateFinance(f["id"], f["asset"], f["acquisition_type"], f["acquisition_date"], f["acquisition_price"], f["actual_price"], f["depreciation_percentage"], f["residual_value"], f["warranty_date"], f["supplier"], f["cost_center"], f["order_id"], f["invoice_id"]))
            self.computers.append()




            


        

    # ==========================================================================================================
    # Helper Functions
    # ==========================================================================================================
    def get_next_url(self, data_dict):
        if 'links' in data_dict and isinstance(data_dict['links'], dict):
            return data_dict['links'].get('next')
        return data_dict.get('next')
        