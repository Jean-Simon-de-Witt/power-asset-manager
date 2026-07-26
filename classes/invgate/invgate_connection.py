import json

import requests
from classes.invgate.invgate_routes import InvgateRoutes as routes
from classes.invgate.invgate_user import InvgateUser
from classes.invgate.invgate_asset import InvgateAsset
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
    def get_data(self, endpoint_path, page = None, v1=False):
        # Ends if not authenticated
        if not self.access_token:
            print("Unable to make request: Not authenticated")
            return None
        
        # Ensure endpoint starts with a slash
        if not endpoint_path.startswith('/'):
            endpoint_path = '/' + endpoint_path

        full_url = f"{self.domain}{endpoint_path}"
        if page:
            full_url = full_url + f"?page={page}"

        try:
            if v1:
                headers = {
                    "Content-Type": "application/vnd.api+json",
                    "Accept": "application/vnd.api+json"
                }
            else:
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            response = self.session.get(full_url, headers=headers)
            response.raise_for_status()
            return response.json()

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
            headers = {
                "Content-Type": "application/vnd.api+json",
                "Accept": "application/vnd.api+json"
            }
            # Requests library automatically formats data correctly for JSON payload when using json=payload
            response = self.session.post(full_url, headers=headers, data=json.dumps(payload))
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
            print("Unable to make request: Not authenticated")
            return None
        
        # Ensure endpoint starts with a slash
        if not endpoint_path.startswith('/'):
            endpoint_path = '/' + endpoint_path

        # Ensure endpoint ends with a slash to prevent 502 Bad Gateway redirect loops
        if not endpoint_path.endswith('/'):
            endpoint_path = endpoint_path + '/'

        full_url = f"{self.domain}{endpoint_path}"

        try:
            # Force the strict JSON:API headers required by InvGate
            headers = {
                "Content-Type": "application/vnd.api+json",
                "Accept": "application/vnd.api+json"
            }
            
            # Use data=json.dumps() so the requests library doesn't overwrite the Content-Type
            response = self.session.put(full_url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"PUT request failed for {endpoint_path}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Server response: {e.response.text}")
                return None
    
    def patch_data(self, endpoint_path, payload):
        if not self.access_token:
            print("Unable to make request: Not authenticated")
            return None
        
        if not endpoint_path.startswith('/'):
            endpoint_path = '/' + endpoint_path

        full_url = f"{self.domain}{endpoint_path}"

        try:
            headers = {
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json"
            }
            response = self.session.patch(full_url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"PATCH request failed for {endpoint_path}: {e}")
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

    # ===========================================================================================
    # Populate Methods: Methods to fetch data from Invgate and instantiate them as Python objects
    # ===========================================================================================

    # Gets a single user from Invgate and returns a User object.
    def get_user(self, id):
        response = self.get_data(routes.user(id))
        user = InvgateUser(name = response.get("name"), id = response.get("id"), email = response.get("email"), date_of_birth = response.get("date_of_birth"), employee_id = response.get("employee_id"), position = response.get("position"), department = response.get("department"), company = response.get("company"), phone = response.get("phone"), cellphone = response.get("cellphone"), address = response.get("address"), person_type = response.get("person_type"), user = response.get("user"), manager = response.get("manager"), location = response.get("location"), cost_center = response.get("cost_center"))
        return user

    # Gets all users on the specified page from Invgate and returns the count, previous page, next page, and a list of User objects. If no page is specified, returns data from the first page.
    def get_users(self, page = None):
        if page:
            response = self.get_data(routes.users(), page = page)
        else:
            response = self.get_data(routes.users())

        if response and response["results"]:
            results = {"count": response.get("count")}

            if response["next"]:
                results["next"] = response.get("next")

            if response["previous"]:
                results["previous"] = response.get("previous")
            users = response.get("results")
            results["users"] = []
            for u in users:
                results["users"].append(InvgateUser(name = u.get("name"), id = u.get("id"), email = u.get("email"), date_of_birth = u.get("date_of_birth"), employee_id = u.get("employee_id"), position = u.get("position"), department = u.get("department"), company = u.get("company"), phone = u.get("phone"), cellphone = u.get("cellphone"), address = u.get("address"), person_type = u.get("person_type"), user = u.get("user"), manager = u.get("manager"), location = u.get("location"), cost_center = u.get("cost_center")))
            return results

        else: 
            print("No results.")
            return None

    def get_finance(self, id):
        response = self.get_data(routes.financial(id))
        finance = InvgateFinance(id = response.get("id"), asset = response.get("asset"), acquisition_type = response.get("acquisition_type"), acquisition_date = response.get("acquisition_date"), acquisition_price = response.get("acquisition_price"), actual_price = response.get("actual_price"), residual_value = response.get("residual_value"), depreciation_percentage = response.get("depreciation_percentage"), warranty_date = response.get("warranty_date"), supplier = response.get("supplier"), cost_center = response.get("cost_center"), order_id = response.get("order_id"), invoice_id = response.get("invoice_id"))
        return finance

    def get_finances(self, page = None):
        if page:
            response = self.get_data(routes.financials(), page = page)
        else:
            response = self.get_data(routes.financials())

        if response and response["results"]:
            results = {"count": response.get("count")}

            if response["next"]:
                results["next"] = response.get("next")

            if response["previous"]:
                results["previous"] = response.get("previous")

            finances = response.get("results")
            results["finances"] = []

            for f in finances:
                results["finances"].append(InvgateFinance(id = f.get("id"), asset = f.get("asset"), acquisition_type = f.get("acquisition_type"), acquisition_date = f.get("acquisition_date"), acquisition_price = f.get("acquisition_price"), actual_price = f.get("actual_price"), residual_value = f.get("residual_value"), depreciation_percentage = f.get("depreciation_percentage"), warranty_date = f.get("warranty_date"), supplier = f.get("supplier"), cost_center = f.get("cost_center"), order_id = f.get("order_id"), invoice_id = f.get("invoice_id")))
            return results
        else:
            print("No results.")
            return None