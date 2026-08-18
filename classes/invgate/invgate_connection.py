import json
import requests
from classes.invgate.invgate_routes import InvgateRoutes as routes
from classes.invgate.invgate_user import InvgateUser
from classes.invgate.invgate_finance import InvgateFinance
from classes.invgate.invgate_vendor import InvgateVendor
from classes.invgate.invgate_tag import InvgateTag
from classes.invgate.invgate_purchase_order import InvgatePurchaseOrder
from classes.invgate.invgate_manufacturer import InvgateManufacturer
from classes.invgate.invgate_health import InvgateHealth
from classes.invgate.invgate_status import InvgateStatus
from classes.invgate.invgate_location import InvgateLocation
from classes.invgate.invgate_software import InvgateSoftware, InvgateVersion, InvgateProgram
from classes.invgate.invgate_update import InvgateUpdate, InvgateOperatingSystemUpdateVersion, InvgateOperatingSystemUpdate
from classes.invgate.invgate_asset import InvgateAsset
from classes.invgate.invgate_computer import *

class InvgateConnection:
    """A class to connect and make requests to the Invgate API.
    """
    # ==============================================================================================
    # Init function: Initializes the connection and attempts to authenticate
    # ==============================================================================================
    def __init__(self, domain: str, client_id: str, client_secret: str):
        """Creates a new InvgateConnection object.

        Args:
            domain (str): The base URL for each route.
            client_id (str): The client ID.
            client_secret (str): The client secret.
        """
        self.domain = domain.rstrip('/')
        self.client_id = client_id
        self.client_secret = client_secret

        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.access_token = None

        self.authenticate()
    # ==============================================================================================
    # Authenticate function: Attempts to authenticate, returns a token if successful.
    # ==============================================================================================
    def authenticate(self):
        """Verifies the given credentials and authenticates the connection if successful.
        """
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
    # Request Methods: General functions that interact directly to the API by sending requests.
    # ==============================================================================================
    def get_data(self, endpoint_path: str = None, page: str = None, v1: bool = False, query: str = None, full_path: str = None, include: list[str] = None) -> dict:
        """Executes GET requests to the API and retrieves data in the form of a dictionary.

        Args:
            endpoint_path (str, optional): The endpoint path to fetch data from. Defaults to None.
            page (str, optional): Used to specify the page to fetch data from. If None, data will be fetched from page 1. Defaults to None.
            v1 (bool, optional): If True, makes a call to version 1 of the Invgate API instead of version 2. Defaults to False.
            query (str, optional): The JSON query parameters to be passed into the request. Defaults to None.
            full_path (str, optional): Specifies the full path to be used for the request rather than the endpoint path. Endpoint path will be ignored if specified along with this parameter. Defaults to None.

        Returns:
            dict: A dictionary of data from the GET request.
        """
        # Ends if not authenticated
        if not self.access_token:
            print("Unable to make request: Not authenticated")
            return None
        
        if endpoint_path:
            if not endpoint_path.startswith('/'):
                endpoint_path = '/' + endpoint_path

        if full_path:
            full_url = full_path
        else:
            if include:
                include_str = "include="
                for i in range(0, len(include)):
                    include_str += include[i]
                    if i < len(include) - 1:
                        include_str += ","
            else:
                include_str = None
                
            full_url = f"{self.domain}{endpoint_path}"
            if page and query and include:
                full_url = full_url + f"?page={page}&{query}&{include_str}"
            elif page and query:
                full_url = full_url + f"?page={page}&{query}"
            elif page and include:
                full_url = full_url + f"?page={page}&{include_str}"
            elif query and include:
                full_url = full_url + f"?{query}&{include_str}"
            elif page:
                full_url = full_url + f"?page={page}"
            elif query:
                full_url = full_url + f"?{query}"
            elif include:
                full_url = full_url + f"?{include_str}"

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

    def post_data(self, endpoint_path: str, payload: dict) -> dict:
        """Adds a new record to Invgate using a POST request.

        Args:
            endpoint_path (str): The endpoint path for data to be posted to.
            payload (dict): A dictionay of the values to be posted.

        Returns:
            dict: The response containing the posted object along with its newly assigned ID.
        """
        
        if not self.access_token:
            print("Unable to make request: Not authenticated")
            return None
        
        # Ensure endpoint starts with a slash
        if not endpoint_path.startswith('/'):
            endpoint_path = '/' + endpoint_path

        full_url = f"{self.domain}{endpoint_path}"

        try:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
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
    
    def patch_data(self, endpoint_path: str, payload: dict) -> dict:
        """Edits the specified fields of a record on Invgate by using a PATCH request.

        Args:
            endpoint_path (str): The endpoint path where data will be patched to.
            payload (dict): A dictionary storing the data to be patched.

        Returns:
            dict: A dictionary containing the patched object with its updated values.
        """
        
        if not self.access_token:
            print("Unable to make request: Not authenticated")
            return None
        
        if not endpoint_path.startswith('/'):
            endpoint_path = '/' + endpoint_path

        full_url = f"{self.domain}{endpoint_path}"

        try:
            headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
            }
            response = self.session.patch(full_url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"PATCH request failed for {endpoint_path}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Server response: {e.response.text}")
                return None

    # ===========================================================================================
    # Populate Methods: Methods to fetch data from Invgate and instantiate them as Python objects
    # ===========================================================================================

    def get_user(self, id: int = None, name: str = None, email: str = None, employee_id: str = None, user_username: str = None) -> InvgateUser:
        """Gets a user from Invgate and returns it as an InvgateUserObject.

        Args:
            id (int, optional): Used to get the user by ID. Defaults to None.
            name (str, optional): Used to get the user by name. Defaults to None.
            email (str, optional): Used to get the user by email. Defaults to None.
            employee_id (str, optional): Used to get the user by employee ID. Defaults to None.
            user_username (str, optional): Used to get the user by username. Defaults to None.

        Returns:
            InvgateUser: The user returned as an InvgateUser object.
        """

        if not self.validate_parameters([id, name, email, employee_id, user_username]):
            print("Get User failed: Please provide one field to get a user by.")
            return None

        query: str = ""
        if id:
            query = f"ids={id}"
        elif name:
            query = f"name={name}"
        elif email:
                query = f"email={email}"
        elif employee_id:
            query = f"employee_id={employee_id}"
        elif user_username:
            query = f"username={user_username}"

        response = self.get_data(endpoint_path = routes.users_detail(), query = query)
        
        if response and response.get("results") and len(response.get("results")) == 1:
            user = response.get("results")[0]

            if user.get("manager"):
                manager_id = user.get("manager").get("id")
                manager_name = user.get("manager").get("name")
                manager_email = user.get("manager").get("email")
            else:
                manager_id: int = ""
                manager_name: str = ""
                manager_email: str = ""

            if user.get("user"):
                user_id: int = user.get("user").get("id")
                username: str = user.get("user").get("username")
            else:
                user_id: int = 0
                username: str = ""

            location: InvgateLocation = self.get_location(id = user.get("location").get("id")) if user.get("location") and user.get("location").get("id") else None

            return InvgateUser(user.get("id") if user.get("id") else 0, user.get("name") or "", user.get("email") or "", user.get("date_of_birth") or "", user.get("employee_id") or "", user.get("position") or "", user.get("department") or "", user.get("company") or "", user.get("phone") or "", user.get("cellphone") or "", user.get("address") or "", user.get("person_type") or "", user_id, username, manager_id, manager_name, manager_email, location, user.get("cost_center") or "")
        print("Get User failed: User not found or invalid response received.")
        return None

    def get_finance(self, id: int) -> InvgateFinance:
        """Gets a finance record from Invgate and returns it as an InvgateFinance object.

        Args:
            id (int): Used to get the finance by ID.

        Returns:
            InvgateFinance: The returned finance as an InvgateFinance object.
        """
      
        response = self.get_data(endpoint_path = routes.financial(id))
        if response:
            vendor = self.get_vendor(response.get("supplier")) if response.get("supplier") else None
            purchase_order = self.get_purchase_order(order_number = response.get("order_id")) if response.get("order_id") else None
            return InvgateFinance(response.get("id") if response.get("id") else 0, response.get("asset") if response.get("asset") else 0, response.get("acquisition_type") or "", response.get("acquisition_date") or "", response.get("acquisition_price") if response.get("acquisition_price") else 0, response.get("actual_price") if response.get("actual_price") else 0, response.get("depreciation_percentage") if response.get("depreciation_percentage") else 0, response.get("residual_value") if response.get("residual_value") else 0, response.get("warranty_date") or "", vendor, response.get("cost_center") or "", purchase_order, response.get("invoice_id") or "")
            
        print("Get Finance failed: Finance not found or invalid response received.")
        return None

    def get_vendor(self, id: int) -> InvgateVendor:
        """Gets a vendor from Invgate and returns it as an InvgateVendor object.

        Args:
            id (int): Used to get the vendor by ID.

        Returns:
            InvgateVendor: The returned vendor as an InvgateVendor object.
        """
     
        response = self.get_data(endpoint_path = routes.vendor(id))
        if response:
            return InvgateVendor(response.get("id") if response.get("id") else 0, response.get("company_name") or "", response.get("legal_name") or "", response.get("status") or "", response.get("country") or "", response.get("tax_id") or "", response.get("website") or "", response.get("address") or "", response.get("email") or "", response.get("billing_currency") or "", response.get("phone") or "", response.get("industry") or "")
        return None

    def get_tag(self, id: int = None, name: str = None) -> InvgateTag:
        """Gets a tag from Invgate and returns it as an InvgateTag object.

        Args:
            id (int, optional): Used to get the tag by ID. Defaults to None.
            name (str, optional): Used to get the tag by name. Defaults to None.

        Returns:
            InvgateTag: The returned tag as an InvgateTag object.
        """

        if not self.validate_parameters([id, name]):
            print("Get Tag failed: Please provide one field to get a tag by.")
            return None
        query = ""
        if id:
            query = f"tag_ids={id}"
        elif name:
            query = f"name={name}"

        response = self.get_data(endpoint_path = routes.tags(), query = query)
        if response and response.get("results") and len(response.get("results")) == 1:
            tag = response.get("results")[0]
            return InvgateTag(tag.get("id") if tag.get("id") else 0, tag.get("name") or "", tag.get("color") or "", tag.get("description") or "", tag.get("smart_tag") if tag.get("smart_tag") else False, tag.get("locked") if tag.get("locked") else False)
        print("Get Tag failed: Tag not found or invalid response received.")
        return None

    def get_purchase_order(self, id: int = None, order_number: str = None) -> InvgatePurchaseOrder:
        """Gets a purchase order from Invgate and returns it as an InvgatePurchaseOrder object.

        Args:
            id (int, optional): Used to get the purchase order by ID. Defaults to None.
            order_number (str, optional): Used to get the purchase order by order number. Defaults to None.

        Returns:
            InvgatePurchaseOrder: The returned purchase order as an InvgatePurchaseOrder object.
        """
        if not self.validate_parameters([id, order_number]):
            print("Get Purchase Order failed: Please provide one field to get a purchase order by.")
            return None
        
        po = None
        if id:
            response = self.get_data(endpoint_path = routes.purchase_order(id))
            po = response if response else None
        elif order_number:
            response = self.get_data(endpoint_path = routes.purchase_orders())
            results = response.get("results") if response else None
            if results:
                for result in results:
                    if result.get("order_number") == order_number:
                        po = result
            else:
                print("Get Purchase Order failed: Purchase Order not found or invalid response received.")
                return None
        if po:
            vendor = self.get_vendor(po.get("vendor")) if po.get("vendor") else None
            return InvgatePurchaseOrder(po.get("id") if po.get("id") else 0, po.get("order_number") or "", vendor, po.get("purchase_order_type") or "", po.get("creation_date") or "", po.get("expected_delivery_date") or "", po.get("date_delivered") or "", po.get("ship_method") or "", po.get("billing_address") or "", po.get("status") or "", po.get("subtotal") if po.get("subtotal") else 0, po.get("freight") or "", po.get("handling") or "", po.get("tax") if po.get("tax") else 0, po.get("total_cost") if po.get("total_cost") else 0, po.get("cost_center") or "", po.get("contract") or "")
        print("Get Purchase Order failed: Purchase Order not found.")
        return None

    def get_manufacturer(self, id: int = None, name: str = None) -> InvgateManufacturer:
        """Gets a manufacturer from Invgate and returns it as an InvgateManufacturer object.

        Args:
            id (int, optional): Used to get the manufacturer by ID. Defaults to None.
            name (str, optional): Used to get the manufacturer by name. Defaults to None.

        Returns:
            InvgateManufacturer: The returned manufacturer as an InvgateManufacturer object.
        """
        if not self.validate_parameters([id, name]):
            print("Get Manufacturer failed: Please provide one field to get a manufacturer by.")
            return None

        manufacturer = None
        if id:
            response = self.get_data(endpoint_path = routes.manufacturer(id))
            manufacturer = response if response else None
        elif name:
            response = self.get_data(endpoint_path = routes.manufacturers(), query = f"name={name}")
            manufacturer = response.get("results")[0] if response and response.get("results") and len(response.get("results")) == 1 else None

        if manufacturer:
            return InvgateManufacturer(manufacturer.get("id") if manufacturer.get("id") else 0, manufacturer.get("name") or "")
        print("Get Manufacturer failed: Manufacturer not found or invalid response received.")
        return None

    def get_health(self, computer_id: int) -> InvgateHealth:
        """Gets a health from Invgate and returns it as an InvgateHealth object.

        Args:
            computer_id (int): Used to get the health by computer ID.

        Returns:
            InvgateHealth: The returned health as an InvgateHealth object.
        """
        response = self.get_data(endpoint_path = routes.health(computer_id))
        if response:
            return InvgateHealth(response.get("id") if response.get("id") else 0, response.get("updated_at") or "", response.get("health_rule") or "", response.get("status") or "")
        print("Get Health failed: Health not found or invalid response received.")
        return None

    def get_status(self, id: int = None, name: str = None) -> InvgateStatus:
        """Gets a status from Invgate and returns it as an InvgateStatus object.

        Args:
            id (int, optional): Used to get the status by ID. Defaults to None.
            name (str, optional): Used to get the status by name. Defaults to None.

        Returns:
            InvgateStatus: The returned status as an InvgateStatus object.
        """
        
        if not self.validate_parameters([id, name]):
            print("Get Status failed: Please provide one parameter to get a status by.")
            return None
        
        query = ""
        if id:
            query = f"ids={id}"
        elif name:
            query = f"name={name}"
        response = self.get_data(endpoint_path = routes.status(), v1 = True, query = query)
        
        if response and response.get("data") and len(response.get("data")) == 1:
            status = response.get("data")[0]
            return InvgateStatus(status.get("id") if status.get("id") else 0, status.get("attributes").get("name") or "", status.get("attributes").get("description") or "", status.get("attributes").get("behavior") or "", status.get("attributes").get("is_default") if status.get("attributes") and status.get("attributes").get("is_default") else False)
        
        print("Get Status failed: Status not found or invalid response received.")
        return None

    def get_location(self, id: int = None, name: str = None) -> InvgateLocation:
        """Gets a location from Invgate and returns it as an InvgateLocation object.

        Args:
            id (int, optional): Used to get the location by ID. Defaults to None.
            name (str, optional): Used to get the location by name. Defaults to None.

        Returns:
            InvgateLocation: The returned location as an InvgateLocation object.
        """
        if not self.validate_parameters([id, name]):
            print("Get Location failed: Please provide one field to get a location by.")
            return None
        
        response = {}
        if id:
            response = self.get_data(endpoint_path = routes.location(id), v1 = True)
        elif name:
            response = self.get_data(endpoint_path = routes.locations(), v1 = True, query = f"name={name}")
        
        if response and response.get("data") and len(response.get("data")) == 1:
            location = response.get("data")[0]
            return InvgateLocation(location.get("id") if location.get("id") else 0, location.get("attributes").get("name") or "", location.get("attributes").get("full_path") or "", location.get("attributes").get("description") or "", location.get("attributes").get("content_type") or "")
        print("Get Location failed: Location not found or invalid response received.")
        return None

    def get_software(self, id: int) -> InvgateSoftware:
        """Gets a software record from Invgate and returns it as an InvgateLocation object.

        Args:
            id (int): Used to get the software by ID.

        Returns:
            InvgateSoftware: The returned software as an InvgateSoftware object.
        """
        response = self.get_data(endpoint_path = routes.software(id))
        if response:
            manufacturer: InvgateManufacturer = InvgateManufacturer(response.get("version").get("program").get("manufacturer").get("id"), response.get("version").get("program").get("manufacturer").get("name") or "") if response.get("version") and response.get("version").get("program") and response.get("version").get("program").get("manufacturer") else None
            program: InvgateProgram = InvgateProgram(response.get("version").get("program").get("name") or "", response.get("version").get("program").get("license") or "", response.get("version").get("program").get("category") or "", response.get("version").get("program").get("types") or "", response.get("version").get("program").get("types_key") or "", response.get("version").get("program").get("tags") or "", response.get("version").get("program").get("is_metering_enabled"), manufacturer) if response.get("version") and response.get("version").get("program") else None
            version: InvgateVersion = InvgateVersion(response.get("version").get("version") or "", response.get("version").get("internal_version") or "", response.get("version").get("edition") or "", program) if response.get("version") else None
            return InvgateSoftware(response.get("id") if response.get("id") else 0, response.get("resource_type") or "", response.get("install_date") or "", response.get("install_path") or "", response.get("uninstall_call") or "", response.get("computer") if response.get("computer") else 0, version) if response.get("version") and response.get("version").get("program") and response.get("version").get("program").get("manufacturer") else None
        print("Get Software failed: Software not found or invalid response received.")

    def get_asset(self, id: int = None, name: str = None, serial: str = None) -> InvgateAsset:
        """Gets an asset from Invgate and returns it as an InvgateAsset object.

        Args:
            id (int, optional): Used to get the asset by ID. Defaults to None.
            name (str, optional): Used to get the asset by name. Defaults to None.
            serial (str, optional): Used to get the asset by serial. Defaults to None.

        Returns:
            InvgateAsset: The returned asset as an InvgateAsset object.
        """
        if not self.validate_parameters([id, name, serial]):
            print("Get Asset failed: please provide one parameter to get an asset by.")
            return None
        
        query = ""
        if id:
            query = f"ids={id}"
        elif name:
            query = f"name={name}"
        elif serial:
            query = f"serial={serial}"

        response = self.get_data(endpoint_path = routes.assets(), query = query)
        
        if response and response.get("results") and len(response.get("results")) == 1:
            asset = response.get("results")[0]
            
            manufacturer: InvgateManufacturer = self.get_manufacturer(name = asset.get("manufacturer")) if asset.get("manufacturer") else None
            finance: InvgateFinance = self.get_finance(id = asset.get("finance")) if asset.get("finance") else None
            owner: InvgateUser = self.get_user(id = asset.get("owner")) if asset.get("owner") else None
            location: InvgateLocation = self.get_location(id = asset.get("location")) if asset.get("location") else None
            status: InvgateStatus = self.get_status(id = asset.get("status")) if asset.get("status") else None
            
            return InvgateAsset(asset.get("id") if asset.get("id") else 0, asset.get("name") or "", manufacturer, asset.get("model") or "", asset.get("commercial_model") or "", asset.get("serial") or "", asset.get("inventory_id") if asset.get("inventory_id") else 0, asset.get("asset_physical_tag") or "", asset.get("physical_identifier_epc") or "", asset.get("created_at") or "", asset.get("reported_at") or "", asset.get("updated_at") or "", finance, asset.get("asset_type") or "", asset.get("asset_type_code") or "", owner, location, status, asset.get("default_ip") or "", asset.get("mac_address") or "", asset.get("format") or "")
        print("Get Asset failed: Asset not found or invalid response received.")
        return None

    def get_update(self, id: int) -> InvgateUpdate:
        """Gets an update from Invgate and returns it as an InvgateUpdate object.

        Args:
            id (int): Used to get the update by ID.

        Returns:
            InvgateUpdate: The returned update as an InvgateUpdate object.
        """
        response = self.get_data(endpoint_path = routes.operating_system_update(id))
        if response:
            os_update: InvgateOperatingSystemUpdate = InvgateOperatingSystemUpdate(response.get("os_update_version").get("os_update").get("short_name") or "", response.get("os_update_version").get("os_update").get("name") or "", response.get("os_update_version").get("os_update").get("update_type") or "", response.get("os_update_version").get("os_update").get("os_type") or "", response.get("os_update_version").get("os_update").get("severity") or "", response.get("os_update_version").get("os_update").get("support_url") or "") if response.get("os_update_version") and response.get("os_update_version").get("os_update") else None
            os_update_version: InvgateOperatingSystemUpdateVersion = InvgateOperatingSystemUpdateVersion(response.get("os_update_version").get("version") or "", response.get("os_update_version").get("release_date") or "", os_update) if response.get("os_update_version") else None
            return InvgateUpdate(response.get("id") if response.get("id") else 0, response.get("install_date") or "", response.get("status") or "", response.get("computer") if response.get("computer") else 0, os_update_version)
        print("Get Update Failed: Update not found or invalid response received.")
        return None
    
    def get_computer(self, asset: InvgateAsset):
        """Gets a computer from Invgate and returns it as an InvgateComputer object.

        Args:
            asset (InvgateAsset): The asset to which the computer is linked.
        """
        response = self.get_data(endpoint_path = routes.computer(asset.id), v1 = True, include = ["reported_motherboard.specs", "reported_bios", "reported_monitors.specs.manufacturer", "reported_printers.specs.manufacturer", "reported_storages.specs.manufacturer", "reported_rams.specs.manufacturer", "reported_cpus.specs.manufacturer", "geolocation", "osinfo_set.os.manufacturer", "osinfo_set.network_adapters.nic", "osinfo_set.gateway", "osinfo_set.dns", "osinfo_set.domains", "osinfo_set.osstatus"])
        included = response.get("included")
        data = response.get("data")
        return self.flatten_data(included, data)
                        
                    
                    
        print("Get Computer failed: Computer not found or invalid response received.")
        return None
    def get_updates_for_computer(self, computer_id: int) -> dict:
        """Gets all updates belonging to an asset and returns them as InvgateUpdate objects.

        Args:
            computer_id (int): The asset's ID.

        Returns:
            dict: A dictionary containing the count of updates and a list of InvgateUpdate objects.
        """
        
        response = self.get_all_pages(self.get_data(endpoint_path = routes.operating_system_updates(), query = f"asset_id={computer_id}"))
        if response and response.get("data"):
            results = {}
            results["count"] = response.get("count")
            results["updates"] = []
            updates = response.get("data")

            for update in updates:
                os_update: InvgateOperatingSystemUpdate = InvgateOperatingSystemUpdate(update.get("os_update_version").get("os_update").get("short_name") or "", update.get("os_update_version").get("os_update").get("name") or "", update.get("os_update_version").get("os_update").get("update_type") or "", update.get("os_update_version").get("os_update").get("os_type") or "", update.get("os_update_version").get("os_update").get("severity") or "", update.get("os_update_version").get("os_update").get("support_url") or "") if update.get("os_update_version") and update.get("os_update_version").get("os_update") else None
                os_update_version: InvgateOperatingSystemUpdateVersion = InvgateOperatingSystemUpdateVersion(update.get("os_update_version").get("version") or "", update.get("os_update_version").get("release_date") or "", os_update) if update.get("os_update_version") else None
                results["updates"].append(InvgateUpdate(update.get("id") if update.get("id") else 0, update.get("install_date") or "", update.get("status") or "", update.get("computer") if update.get("computer") else 0, os_update_version))
            return results
        print("Get Software failed: No results or invalid response received.")
        return None

    def get_software_for_computer(self, computer_id: int) -> dict:
        """Gets all software belonging to an asset and returns them as InvgateSoftware objects.

        Args:
            computer_id (int): The asset's ID.

        Returns:
            dict: A dictionary containing the count of software and a list of InvgateSoftware objects.
        """
        
        response = self.get_all_pages(self.get_data(endpoint_path = routes.manufacturers()))
        manufacturers: dict[int, InvgateManufacturer] = {}
        if response and response.get("data"):
            for manufacturer in response.get("data"):
                manufacturers[manufacturer.get("id")] = InvgateManufacturer(manufacturer.get("id"), manufacturer.get("name"))

        response = self.get_all_pages(self.get_data(endpoint_path = routes.softwares(), query = f"asset_id={computer_id}"))
        if response and response.get("data"):
            results = {}
            results["count"] = response.get("count")
            results["software"] = []
            softwares = response.get("data")

            for software in softwares:
                manufacturer: InvgateManufacturer = manufacturers.get(software.get("version").get("program").get("manufacturer").get("id")) if software.get("version") and software.get("version").get("program") and software.get("version").get("program").get("manufacturer") and manufacturers.get(software.get("version").get("program").get("manufacturer").get("id")) else None
                program: InvgateProgram = InvgateProgram(software.get("version").get("program").get("name") or "", software.get("version").get("program").get("license") or "", software.get("version").get("program").get("category") or "", software.get("version").get("program").get("types") or "", software.get("version").get("program").get("types_key") or "", software.get("version").get("program").get("tags") or "", software.get("version").get("program").get("is_metering_enabled"), manufacturer) if software.get("version") and software.get("version").get("program") else None
                version: InvgateVersion = InvgateVersion(software.get("version").get("version") or "", software.get("version").get("internal_version") or "", software.get("version").get("edition") or "", program) if software.get("version") else None
                results["software"].append(InvgateSoftware(software.get("id") if software.get("id") else 0, software.get("resource_type") or "", software.get("install_date") or "", software.get("install_path") or "", software.get("uninstall_call") or "", software.get("computer") if software.get("computer") else 0, version))
            return results

    def get_asset_with_collections(self, id: int = None, name: str = None, serial: str = None) -> InvgateAsset:
        """Gets an asset from Invgate with its health, software, and updates and returns it as an InvgateAsset object.

        Args:
            id (int, optional): Used to get the asset by ID. Defaults to None.
            name (str, optional): Used to get the asset by name. Defaults to None.
            serial (str, optional): Used to get the asset by serial. Defaults to None.

        Returns:
            InvgateAsset: The returned asset as an InvgateAsset object.
        """
        
        if not self.validate_parameters([id, name, serial]):
            print("Get Asset failed: please provide one parameter to get an asset by.")
            return None
        
        query = ""
        if id:
            query = f"ids={id}"
        elif name:
            query = f"name={name}"
        elif serial:
            query = f"serial={serial}"

        response = self.get_data(endpoint_path = routes.assets(), query = query)
        
        if response and response.get("results") and len(response.get("results")) == 1:
            asset = response.get("results")[0]
            
            manufacturer: InvgateManufacturer = self.get_manufacturer(name = asset.get("manufacturer")) if asset.get("manufacturer") else None
            finance: InvgateFinance = self.get_finance(id = asset.get("finance")) if asset.get("finance") else None
            owner: InvgateUser = self.get_user(id = asset.get("owner")) if asset.get("owner") else None
            location: InvgateLocation = self.get_location(id = asset.get("location")) if asset.get("location") else None
            status: InvgateStatus = self.get_status(id = asset.get("status")) if asset.get("status") else None
            
            asset_object = InvgateAsset(asset.get("id") if asset.get("id") else 0, asset.get("name") or "", manufacturer, asset.get("model") or "", asset.get("commercial_model") or "", asset.get("serial") or "", asset.get("inventory_id") if asset.get("inventory_id") else 0, asset.get("asset_physical_tag") or "", asset.get("physical_identifier_epc") or "", asset.get("created_at") or "", asset.get("reported_at") or "", asset.get("updated_at") or "", finance, asset.get("asset_type") or "", asset.get("asset_type_code") or "", owner, location, status, asset.get("default_ip") or "", asset.get("mac_address") or "", asset.get("format") or "")

            health: InvgateHealth = self.get_health(asset.get("id"))
            software: list[InvgateSoftware] = self.get_software_for_computer(asset.get("id"))
            updates: list[InvgateUpdate] = self.get_updates_for_computer(asset.get("id"))
            asset_object.populate_collections(health = health if health else None, software = software.get("software") if software else None, updates = updates.get("updates") if updates else None)
        print("Get Asset failed: Asset not found or invalid response received.")
        return None
                
    def load_data(self) -> dict:
        """A bulk method that loads all data from Invgate as a dictionary containing lists of each relevant object.

        Returns:
            dict: The dictionary that contains the data. Contains a list of InvgateUser objects and a list of InvgateAsset objects.
        """

        results = {}

        # Vendors
        temp_vendors: dict[int, InvgateVendor] = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.vendors()))
        for vendor in response.get("data"):
            temp_vendors[vendor.get("id")] = InvgateVendor(vendor.get("id") if vendor.get("id") else 0, vendor.get("company_name") or "", vendor.get("legal_name") or "", vendor.get("status") or "", vendor.get("tax_id") or "", vendor.get("country") or "", vendor.get("website") or "", vendor.get("address") or "", vendor.get("email") or "", vendor.get("billing_currency") or "", vendor.get("phone") or "", vendor.get("industry") or "")

        # Manufacturers
        temp_manufacturers: dict[str, InvgateManufacturer] = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.manufacturers()))
        for manufacturer in response.get("data"):
            temp_manufacturers[manufacturer.get("name")] = InvgateManufacturer(manufacturer.get("id") if manufacturer.get("id") else 0, manufacturer.get("name") or "")

        # Locations
        temp_locations: dict[int, InvgateLocation] = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.locations(), v1 = True))
        for location in response.get("data"):
            temp_locations[location.get("id")] = InvgateLocation(location.get("id") if location.get("id") else 0, location.get("attributes").get("name") or "", location.get("attributes").get("full_path") or "", location.get("attributes").get("description") or "", location.get("attributes").get("content_type") or "")
        # Statuses
        temp_statuses: dict[int, InvgateStatus] = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.status(), v1 = True))
        for status in response.get("data"):
            temp_statuses[status.get("id")] = InvgateStatus(status.get("id") if status.get("id") else 0, status.get("attributes").get("name") or "", status.get("attributes").get("description") or "", status.get("attributes").get("behavior") or "", status.get("attributes").get("is_default") if status.get("attributes").get("is_default") else False)
        # Purchase Orders
        temp_purchase_orders: dict[str, InvgatePurchaseOrder] = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.purchase_orders()))
        for po in response.get("data"):
            vendor = temp_vendors.get(po.get("vendor")) if po.get("vendor") else None
            temp_purchase_orders[po.get("order_number")] = InvgatePurchaseOrder(po.get("id") if po.get("id") else 0, po.get("order_number") or "", vendor, po.get("purchase_order_type") or "", po.get("creation_date") or "", po.get("expected_delivery_date") or "", po.get("date_delivered") or "", po.get("ship_method") or "", po.get("billing_address") or "", po.get("status") or "", po.get("subtotal") if po.get("subtotal") else 0, po.get("freight") or "", po.get("handling") or "", po.get("tax") if po.get("tax") else 0, po.get("total_cost") if po.get("total_cost") else 0, po.get("cost_center") or "", po.get("contract") or "")
        # Finance
        temp_finance: dict[int, InvgateFinance] = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.financials()))
        for finance in response.get("data"):
            vendor = temp_vendors.get(finance.get("vendor")) if finance.get("vendor") else None
            purchase_order = temp_purchase_orders.get(finance.get("order_id")) if finance.get("order_id") else None

            temp_finance[finance.get("id")] = InvgateFinance(finance.get("id") if finance.get("id") else 0, finance.get("asset") if finance.get("asset") else 0, finance.get("acquisition_type") or "", finance.get("acquisition_date") or "", finance.get("acquisition_price") if finance.get("acquisition_price") else 0, finance.get("actual_price") if finance.get("actual_price") else 0, finance.get("depreciation_percentage") if finance.get("depreciation_percentage") else 0, finance.get("residual_value") if finance.get("residual_value") else 0, finance.get("warranty_date") or "", vendor, finance.get("cost_center") or "", purchase_order, finance.get("invoice_id") or "")

        # Users
        response = self.get_all_pages(self.get_data(endpoint_path = routes.users_detail()))
        temp_users: dict[int, InvgateUser] = {}
        results["users"] = []
        for user in response.get("data"):
            if user.get("manager"):
                manager_id = user.get("manager").get("id")
                manager_name = user.get("manager").get("name")
                manager_email = user.get("manager").get("email")
            else:
                manager_id = None
                manager_name = None
                manager_email = None
            if user.get("user"):
                user_id = user.get("user").get("id")
                username = user.get("user").get("username")
            else:
                user_id = None
                username = None                

            location = temp_locations.get(user.get("location").get("id")) if user.get("location") and user.get("location").get("id") else None
            user_object = InvgateUser(user.get("id") if user.get("id") else 0, user.get("name") or "", user.get("email") or "", user.get("date_of_birth") or "", user.get("employee_id") or "", user.get("position") or "", user.get("department") or "", user.get("company") or "", user.get("phone") or "", user.get("cellphone") or "", user.get("address") or "", user.get("person_type") or "", user_id, username, manager_id, manager_name, manager_email, location, user.get("cost_center") or "")
            temp_users[user_object.id] = user_object
            results["users"].append(user_object)

        # Assets
        results["assets"] = []
        response = self.get_all_pages(self.get_data(endpoint_path = routes.assets()))
        for asset in response.get("data"):
            status = temp_statuses.get(asset.get("status")) if asset.get("status") else None
            location = temp_locations.get(asset.get("location")) if asset.get("location") else None
            owner = temp_users.get(asset.get("owner")) if asset.get("owner") else None
            finance = temp_finance.get(asset.get("finance")) if asset.get("finance") else None
            manufacturer = temp_manufacturers.get(asset.get("manufacturer")) if asset.get("manufacturer") else None

            results["assets"].append(InvgateAsset(asset.get("id") if asset.get("id") else 0, asset.get("name") or "", manufacturer, asset.get("model") or "", asset.get("commercial_model") or "", asset.get("serial") or "", asset.get("inventory_id") if asset.get("inventory_id") else 0, asset.get("asset_physical_tag") or "", asset.get("physical_identifier_epc") or "", asset.get("created_at") or "", asset.get("reported_at") or "", asset.get("updated_at") or "", finance, asset.get("asset_type") or "", asset.get("asset_type_code") or "", owner, location, status, asset.get("default_ip"), asset.get("mac_address") or "", asset.get("format") or ""))

        return results

    # =============================================================================================
    # Create Methods: Methods to export data from Python objects and create new objects in Invgate.
    # =============================================================================================

    def create_asset(self, asset: InvgateAsset) -> InvgateAsset:
        """Creates a new asset in Invgate.

        Args:
            asset (InvgateAsset): The asset to be created.

        Returns:
            InvgateAsset: The created asset along with its newly assigned ID.
        """
        
        response = self.post_data(endpoint_path = routes.assets(), payload = asset.to_json())

        if response.get("id"):
            status: InvgateStatus = self.get_status(id = response.get("status")) if response.get("status") else None
            location: InvgateLocation = self.get_location(id = response.get("location")) if response.get("location") else None
            owner: InvgateUser = self.get_user(id = response.get("owner")) if response.get("owner") else None
            finance: InvgateFinance = self.get_finance(id = response.get("finance")) if response.get("finance") else None
            manufacturer: InvgateManufacturer = self.get_manufacturer(id = response.get("manufacturer")) if response.get("manufacturer") else None

            return InvgateAsset(response.get("id"), response.get("name") or "", manufacturer, response.get("model") or "", response.get("commercial_model") or "", response.get("serial") or "", response.get("inventory_id") or "", response.get("asset_physical_tag") or "", response.get("physical_identifier_epc") or "", response.get("created_at") or "", response.get("reported_at") or "", response.get("updated_at") or "", finance, response.get("asset_type") or "", response.get("asset_type_code") or "", owner, location, status, response.get("default_ip") or "", response.get("mac_address") or "", response.get("format") or "")
        return None

    def create_user(self, user: InvgateUser) -> InvgateUser:
        """Creates a new user in Invgate.

        Args:
            user (InvgateUser): The user to be created.

        Returns:
            InvgateUser: The created user along with its newly assigned ID.
        """
        response = self.post_data(endpoint_path = routes.users(), payload = user.to_json())

        if response.get("id"):
            manager = self.get_user(id = response.get("manager")) if response.get("manager") else None
            if manager:
                manager_id = manager.id
                manager_name = manager.name
                manager_email = manager.email
                
            location = self.get_location(id = response.get("location")) if response.get("location") else None
            if response.get("user"):
                user_id = response.get("user").get("id")
                username = response.get("user").get("username")
            else:
                user_id = 0
                username = ""

            return InvgateUser(response.get("id"), response.get("name") or "", response.get("email") or "", response.get("date_of_birth") or "", response.get("employee_id"), response.get("position"), response.get("department") or "", response.get("company") or "", response.get("phone") or "", response.get("cellphone") or "", response.get("address") or "", response.get("person_type") or "", user_id, username, manager_id, manager_name, manager_email, location, response.get("cost_center") or None)
        return None

    # ==================================================================================================
    # Update Methods: Methods to export data from Python objects and update existing objects in Invgate.
    # ==================================================================================================

    def update_asset(self, asset: InvgateAsset) -> InvgateAsset:
        """Updates the specified data of an existing asset in Invgate.

        Args:
            asset (InvgateAsset): The asset to be edited.

        Returns:
            InvgateAsset: The edited asset with its updated values.
        """
        response = self.patch_data(endpoint_path = routes.asset(asset.id), payload = asset.to_json())

        if response.get("id"):
            status: InvgateStatus = self.get_status(id = response.get("status")) if response.get("status") else None
            location: InvgateLocation = self.get_location(id = response.get("location")) if response.get("location") else None
            owner: InvgateUser = self.get_user(id = response.get("owner")) if response.get("owner") else None
            finance: InvgateFinance = self.get_finance(id = response.get("finance")) if response.get("finance") else None
            manufacturer: InvgateManufacturer = self.get_manufacturer(id = response.get("manufacturer")) if response.get("manufacturer") else None

            return InvgateAsset(response.get("id"), response.get("name") or "", manufacturer, response.get("model") or "", response.get("commercial_model") or "", response.get("serial") or "", response.get("inventory_id") or "", response.get("asset_physical_tag") or "", response.get("physical_identifier_epc") or "", response.get("created_at") or "", response.get("reported_at") or "", response.get("updated_at") or "", finance, response.get("asset_type") or "", response.get("asset_type_code") or "", owner, location, status, response.get("default_ip") or "", response.get("mac_address") or "", response.get("format") or "")
        return None

    def update_user(self, user: InvgateUser) -> InvgateUser:
        """Updates the specified data of an existing asset in Invgate.

        Args:
            user (InvgateUser): The user to be edited.

        Returns:
            InvgateUser: The edited user with its updated values.
        """
        response = self.patch_data(endpoint_path = routes.user(user.id), payload = user.to_json())

        if response.get("id"):
            manager = self.get_user(id = response.get("manager")) if response.get("manager") else None
            if manager:
                manager_id = manager.id
                manager_name = manager.name
                manager_email = manager.email
            else:
                manager_id = 0
                manager_name = ""
                manager_email = ""
                
            location = self.get_location(id = response.get("location")) if response.get("location") else None
            if response.get("user"):
                user_id = response.get("user").get("id")
                username = response.get("user").get("username")
            else:
                user_id = 0
                username = ""

            return InvgateUser(response.get("id"), response.get("name") or "", response.get("email") or "", response.get("date_of_birth") or "", response.get("employee_id"), response.get("position"), response.get("department") or "", response.get("company") or "", response.get("phone") or "", response.get("cellphone") or "", response.get("address") or "", response.get("person_type") or "", user_id, username, manager_id, manager_name, manager_email, location, response.get("cost_center") or None)
        return None

# ================================================
# Helper Functions
# ================================================
    def get_all_pages(self, response: dict) -> dict:
        """A helper function to get all paginated values for a GET request.

        Args:
            response (dict): The response returned from get_data().

        Returns:
            dict: A dictionary of the data stored as dictionaries.
        """
        if response:
            results: dict = {}
            results["data"] = []
            if response.get("results"):
                results["count"] = response.get("count")
                while True:
                    results["data"].extend(response.get("results"))

                    if not response.get("next"):
                        break
                    elif response.get("next") == "None":
                        break
                    else:
                        response = self.get_data(full_path = response.get("next"))
                        
                        if not response:
                            break
            elif response.get("data"):
                results["count"] = 0
                while True:
                    results["count"] += len(response.get("data"))
                    results["data"].extend(response.get("data"))

                    links = response.get("links") if response.get("links") else {}
                    if not links.get("next") or links.get("next") == "None":
                        break
                    elif links.get("next") == "None":
                        break
                    else:
                        response = self.get_data(full_path = links.get("next"))
                        
                        if not response:
                            break
            else:
                return response

            return results
        else:
            return None

    def validate_parameters(self, parameters: list) -> bool:
        """A helper function used to validate whether or not the correct number of parameters were specified for a method.

        Args:
            parameters (list): All possible parameters for the function.

        Returns:
            bool: Whether or not the correct number of parameters were specified.
        """
        count_parameters: int = 0
        for parameter in parameters:
            if parameter:
                count_parameters += 1

        if count_parameters != 1:
            return False
        return True
    
    def map_included_data(self, included_data: list[dict]) -> dict[str, dict[str, any]]:
        """A helper function used to map included data based on their type and their ID.

        Args:
            included_data (list[dict]): The set of included data to map.

        Returns:
            dict[str, dict[str, any]]: The mapped set of relations.
        """
        mapped_data: dict[str, dict[str, any]] = {}
        
        for data in included_data:
            r_type = data.get("type") if data.get("type") else None
            
            if r_type and data.get("id"):
                if not mapped_data.get(r_type):
                    mapped_data[r_type] = {}
                mapped_data[r_type][data.get("id")] = data
            else:
                continue
            
        return mapped_data
    
    def get_related_data(self, data: dict[str, dict[str, any]], object: dict[str, any], mapped: bool = False) -> dict[str, dict[str, any]]:
        if data:
            if not mapped:
                mapped_data = self.map_included_data(data)
            else:
                mapped_data = data
        else:
            return None
        relationships = object.get("relationships")
        related_data: dict[str, dict[str, any]] = {}
        if relationships:
            for key, relationship in relationships.items():
                if relationship.get("meta"):
                    contained_values = relationship.get("data")
                    if contained_values:
                        related_data[key] = []
                        for contained_value in contained_values:
                            matched_data = mapped_data.get(contained_value.get("type")).get(contained_value.get("id")) if mapped_data.get(contained_value.get("type")) and mapped_data.get(contained_value.get("type")).get(contained_value.get("id")) else None
                            if matched_data:
                                related_data.get(key).append(matched_data)
                            else:
                                continue
                    else:
                        continue
                else:
                    matched_data = mapped_data.get(relationship.get("type")).get(relationship.get("id")) if mapped_data.get(relationship.get("type")) and mapped_data.get(relationship.get("type")).get(relationship.get("id")) else None
                    if matched_data:
                        related_data[key] = matched_data
                    else:
                        continue
            return related_data
        return None
    def flatten_data(self, included_data: dict[str, dict[str, any]], obj: dict[str, any], mapped: bool = False) -> dict[str, any]:
        if included_data:
            if not mapped:
                mapped_data = self.map_included_data(included_data)
            else:
                mapped_data = included_data
        else:
            return None
        
        flattened_data = {}
        attributes = obj.get("attributes")
        
        if attributes and obj.get("id") and obj.get("type"):
            flattened_data["id"] = obj.get("id")
            flattened_data["type"] = obj.get("type")
        for key, value in attributes.items():
            if key == "relationships":
                continue
            flattened_data[key] = value
        relationships = self.get_related_data(mapped_data, obj, mapped = True)
        if relationships:
            for r_key, relationship in relationships.items():
                if type(relationship) == list:
                    flattened_data[r_key] = []
                    for contained_item in relationship:
                        flattened_data[r_key].append(self.flatten_data(mapped_data, contained_item, mapped = True))
                else:
                    flattened_data[r_key] = self.flatten_data(mapped_data, relationship, mapped = True)
                
        return flattened_data