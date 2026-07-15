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
            # Make the FIRST request exactly as provided
            response = self.session.get(full_url)
            response.raise_for_status()
            response_json = response.json()

            # Check how InvGate formatted the response
            list_key = 'data' if 'data' in response_json else 'results'

            # ==========================================
            # BRANCH 1: LIST OF ITEMS (PAGINATION)
            # ==========================================
            if list_key in response_json and isinstance(response_json[list_key], list):
                all_data = []
                all_included = []
                
                all_data.extend(response_json[list_key]) 
                if "included" in response_json:
                    all_included.extend(response_json["included"])

                next_url = self.get_next_url(response_json)
                
                # Loop through remaining pages
                while next_url:
                    if not next_url.startswith('http'):
                        next_url = f"{self.domain}{next_url}"

                    # Fix the comma encoding bug
                    next_url = next_url.replace("%2C", ",")

                    response = self.session.get(next_url)
                    response.raise_for_status()
                    response_json = response.json()
                    
                    all_data.extend(response_json[list_key])

                    if "included" in response_json:
                        all_included.extend(response_json["included"])

                    next_url = self.get_next_url(response_json)
                    
                # --> RETURN LOGIC FOR LISTS ONLY <--
                if all_included:
                    return {"data": all_data, "included": all_included}
                else:
                    return all_data

            # ==========================================
            # BRANCH 2: SINGLE RECORD
            # ==========================================
            else:
                # E.g. User 888 or Finance 919
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
        print("Populating data...")
        self.populate_users()
        self.populate_computers()
        print("Data populated")

    # Gets all users and stores them as classes in memory
    def populate_users(self):
        self.users = []
        user_data = self.get_users()

        for u in user_data:
            u_id = u.get("id")
            a = u.get("attributes")
            user = InvgateUser(u_id, a["name"], a["email"], a["email_display"], a["date_of_birth"], a["person_id"], a["position"], a["department"], a["company"], a["phone"], a["cellphone"], a["address"], a["person_type"], a["is_deleted"])
            self.users.append(user)

    def populate_computers(self):
        self.computers = []
        
        extracted_data = self.get_computers()
        
        if not extracted_data:
            print("Warning: Could not fetch computers. Skipping population.")
            return

        if isinstance(extracted_data, list):
            computer_data = extracted_data
            included_data = []
        else:
            computer_data = extracted_data.get("data", [])
            included_data = extracted_data.get("included", [])

        # 1. Build the Hardware Specs Lookup Dictionary
        included_lookup = {}
        for item in included_data:
            item_type = item.get("type")
            item_id = item.get("id")
            if item_type not in included_lookup:
                included_lookup[item_type] = {}
            included_lookup[item_type][item_id] = item

        # 2. Build the Bulk Finance Lookup Dictionary
        finance_raw_data = self.get_data(routes.financials())
        
        if isinstance(finance_raw_data, list):
            finance_list = finance_raw_data
        else:
            finance_list = finance_raw_data.get("data", []) if finance_raw_data else []
            
        finance_lookup = {}
        for record in finance_list:
            f_id = str(record.get("id"))
            finance_lookup[f_id] = record

        # Helper Function for 3-Jump hardware lookups
        def get_hardware_details(relationship_data, expected_reported_type, expected_model_type):
            if not relationship_data:
                return {}, {}
            
            pointer = relationship_data[0] if isinstance(relationship_data, list) else relationship_data
            reported_item = included_lookup.get(expected_reported_type, {}).get(pointer.get("id"), {})
            
            model_pointer = reported_item.get("relationships", {}).get("specs", {}).get("data", {})
            model_item = {}
            if model_pointer:
                model_item = included_lookup.get(expected_model_type, {}).get(model_pointer.get("id"), {})
                
            man_pointer = model_item.get("relationships", {}).get("manufacturer", {}).get("data", {})
            man_item = {}
            if man_pointer:
                man_item = included_lookup.get("Manufacturer", {}).get(man_pointer.get("id"), {})
                
            return model_item, man_item
        # ---------------------------------------

        # 3. Loop through all computers and build class instances
        for c in computer_data:
            c_id = c.get("id")
            a = c.get("attributes", {})
            r = c.get("relationships", {})

            # Get hardware spec items
            cpu_model, cpu_man = get_hardware_details(r.get("reported_cpus", {}).get("data"), "ReportedCPU", "CPUModel")
            cpu_attrs = cpu_model.get("attributes", {})
            cpu_man_attrs = cpu_man.get("attributes", {})

            ram_model, ram_man = get_hardware_details(r.get("reported_rams", {}).get("data"), "ReportedRAMModule", "RAMModuleModel")
            ram_attrs = ram_model.get("attributes", {})
            ram_man_attrs = ram_man.get("attributes", {})

            mb_model, mb_man = get_hardware_details(r.get("reported_motherboard", {}).get("data"), "ReportedMotherboard", "MotherboardModel")
            mb_attrs = mb_model.get("attributes", {})
            mb_man_attrs = mb_man.get("attributes", {})

            # Get finance data
            finance_pointer = r.get("finance", {}).get("data")
            f = {}
            if finance_pointer:
                target_finance_id = str(finance_pointer.get("id"))
                raw_f = finance_lookup.get(target_finance_id, {})
                f = raw_f.get("attributes", raw_f)

            # ==========================================
            # Extract Wi-Fi MAC Address via OSInfo jump
            # ==========================================
            wifi_mac = None
            osinfo_pointer = r.get("osinfo_set", {}).get("data", [])
            
            if osinfo_pointer:
                os_id = osinfo_pointer[0].get("id")
                os_record = included_lookup.get("OSInfo", {}).get(os_id, {})
                
                adapters_pointer = os_record.get("relationships", {}).get("network_adapters", {}).get("data", [])
                
                for adapter in adapters_pointer:
                    adapter_id = adapter.get("id")
                    adapter_record = included_lookup.get("NetworkAdapter", {}).get(adapter_id, {})
                    
                    mac = adapter_record.get("attributes", {}).get("mac")
                    device_type = adapter_record.get("attributes", {}).get("device_id", "")
                    
                    if mac and device_type == "Wi-Fi":
                        wifi_mac = mac
                        break  # Match found, terminate search loop
            # ==========================================

            computer = InvgateComputer(
                c_id,
                a.get("total_storage"), 
                a.get("total_ram"), 
                a.get("format_type"), 
                a.get("name"), 
                a.get("inventory_id"), 
                a.get("serial"), 
                a.get("virtual"), 
                a.get("match_field"), 
                a.get("firewall_status"), 
                a.get("status"), 
                a.get("antivirus_status"), 
                a.get("connection_status"), 
                a.get("lifecycle_status"), 
                
                # We append our new wifi_mac field right here
                wifi_mac,
                
                InvgateMotherboard(
                    mb_model.get("id"), mb_attrs.get("model"), 
                    mb_man_attrs.get("name"), mb_man.get("id"), mb_man_attrs.get("support_url"), mb_man_attrs.get("website_url")
                ), 
                InvgateCPU(
                    cpu_model.get("id"), cpu_attrs.get("model_name"), cpu_attrs.get("model"), cpu_attrs.get("kind"), cpu_attrs.get("import_uuid"), cpu_attrs.get("updated_at"), cpu_attrs.get("family"), cpu_attrs.get("frequency"), cpu_attrs.get("cores"), 
                    cpu_man.get("id"), cpu_man_attrs.get("name"), cpu_man_attrs.get("support_url"), cpu_man_attrs.get("website_url")
                ), 
                InvgateRAM(
                    ram_model.get("id"), ram_attrs.get("model_name"), ram_attrs.get("model"), ram_attrs.get("kind"), ram_attrs.get("import_uuid"), ram_attrs.get("updated_at"), ram_attrs.get("capacity"), ram_attrs.get("speed"), ram_attrs.get("device_type"), ram_attrs.get("width"), 
                    ram_man.get("id"), ram_man_attrs.get("name"), ram_man_attrs.get("support_url"), ram_man_attrs.get("website_url")
                ), 
                InvgateFinance(
                    f.get("id"), f.get("asset"), f.get("acquisition_type"), f.get("acquisition_date"), f.get("acquisition_price"), f.get("actual_price"), f.get("depreciation_percentage"), f.get("residual_value"), f.get("warranty_date"), f.get("supplier"), f.get("cost_center"), f.get("order_id"), f.get("invoice_id")
                )
            )
            
            self.computers.append(computer)

    def get_computer_by_id(self, computer_id) -> InvgateComputer:
        for computer in self.computers:
            if computer.id == computer_id:
                return computer
            
    def get_computer_by_name(self, computer_name) -> InvgateComputer:
        for computer in self.computers:
            if computer.name == computer_name:
                return computer
            
    def get_computer_by_mac(self, mac_address) -> InvgateComputer:
        for computer in self.computers:
            if computer.mac_address == mac_address:
                return computer 



            


        

    # ==========================================================================================================
    # Helper Functions
    # ==========================================================================================================
    def get_next_url(self, data_dict):
        if 'links' in data_dict and isinstance(data_dict['links'], dict):
            return data_dict['links'].get('next')
        return data_dict.get('next')
    
        