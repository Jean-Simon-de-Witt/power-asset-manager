import requests
from classes.invgate_routes import InvgateRoutes as routes

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

        try:
            all_data = []
            page = 1

            while True:
                separator = '&' if '?' in endpoint_path else '?'
                paginated_url = f"{self.domain}{endpoint_path}{separator}page={page}"

                response = self.session.get(paginated_url)
                response.raise_for_status()

                response_json = response.json()
                list_key = 'data' if 'data' in response_json else 'results'

                if list_key in response_json:
                    if isinstance(response_json[list_key], list):
                        all_data.extend(response_json[list_key])

                        if response_json.get('next'):
                            page += 1
                        else:
                            break
                    else:
                        return response_json
                else:
                    return response_json
            return all_data
                
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

    def get_user(self, id):
        endpoint_path = routes.user(id)
        return self.get_data(endpoint_path)