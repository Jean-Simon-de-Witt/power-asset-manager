import requests

class InvgateConnection:
    # =================================================================================
    # Init function: Initializes the connection and attempts to authenticate
    # =================================================================================
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

    # =================================================================================
    # Authenticate function: Attempts to authenticate, returns a token if successful.
    # =================================================================================
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

    # =================================================================================
    # Get Data function: Makes GET requests to the API using the authenticated session.
    # =================================================================================
    def get_data(self, endpoint_path):
        # Ends function if not authenticated
        if not self.access_token:
            print("Unable to make request: Not authenticated")
            return None
        
        # Ensure endpoint starts with a slash
        if not endpoint_path.startswith('/'):
            endpoint_path = '/' + endpoint_path
        
        full_url = f"{self.domain}{endpoint_path}"

        try:
            response = self.session.get(full_url)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"GET request failed for {endpoint_path}: {e}")
            return None