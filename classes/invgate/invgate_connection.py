import json
import requests
from typing import Any
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
        
        if response and response.get("results") and len(response.get("results")) >= 1:
            if len(response.get("results")) > 1:
                active_result = False
                asset = None
                for result in response.get("results"):
                    if result.get("status") == 2:
                        active_result = True
                        asset = result
                if not active_result:
                    asset = response.get("results")[0]
            else:
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
    
    def get_computer(self, asset: InvgateAsset) -> InvgateComputer:
        """Gets a computer from Invgate and returns it as an InvgateComputer object.

        Args:
            asset (InvgateAsset): The asset to which the computer is linked.
        """
        response = self.get_data(endpoint_path = routes.computer(asset.id), v1 = True, include = ["reported_motherboard.specs", "reported_bios", "reported_monitors.specs.manufacturer", "reported_printers.specs.manufacturer", "reported_storages.specs.manufacturer", "reported_rams.specs.manufacturer", "reported_cpus.specs.manufacturer", "geolocation", "osinfo_set.os.manufacturer", "osinfo_set.network_adapters.nic", "osinfo_set.gateway", "osinfo_set.dns", "osinfo_set.domains", "osinfo_set.osstatus"])
        included = response.get("included")
        mapped_data = self.map_included_data(included)
        computer = self.flatten_data(mapped_data, response.get("data"))
        
        # OS Info
        osinfos: list[dict[str, Any]] = computer.get("osinfo_set") if computer.get("osinfo_set") else None
        if osinfos:
            osinfo_set: list[ReportedOSInfo] = []
            for osinfo_d in osinfos:
                os_d = osinfo_d.get("os") if osinfo_d.get("os") else None
                if os_d:
                    manufacturer_d = os_d.get("manufacturer") if os_d.get("manufacturer") else None
                    if manufacturer_d:
                        manufacturer: ReportedManufacturer = ReportedManufacturer(manufacturer_d.get("id") or "", manufacturer_d.get("name") or "", manufacturer_d.get("is_manual") if manufacturer_d.get("is_manual") else False, manufacturer_d.get("is_component") if manufacturer_d.get("is_component") else False, manufacturer_d.get("logo") or "", manufacturer_d.get("support_url") or "", manufacturer_d.get("website_url") or "")
                    else:
                        manufacturer: ReportedManufacturer = None
                    os: ReportedOS = ReportedOS(os_d.get("id") or "", os_d.get("name") or "", os_d.get("version") or "", os_d.get("arch") or "", os_d.get("full_name") or "", os_d.get("supports_software_deployment") if os_d.get("supports_software_deployment") else False, manufacturer)
                else:
                    os: ReportedOS = None
                network_adapters_d = osinfo_d.get("network_adapters") if osinfo_d.get("network_adapters") else None
                if network_adapters_d:
                    network_adapters: list[ReportedNetworkAdapter] = []
                    for network_adapter_d in network_adapters_d:
                        model_d = network_adapter_d.get("nic") if network_adapter_d.get("nic") else None
                        if model_d:
                            manufacturer_d = model_d.get("manufacturer") if model_d.get("manufacturer") else None
                            if manufacturer_d:
                                manufacturer: ReportedManufacturer = ReportedManufacturer(manufacturer_d.get("id") or "", manufacturer_d.get("name") or "", manufacturer_d.get("is_manual") if manufacturer_d.get("is_manual") else False, manufacturer_d.get("is_component") if manufacturer_d.get("is_component") else False, manufacturer_d.get("logo") or "", manufacturer_d.get("support_url") or "", manufacturer_d.get("website_url") or "")
                            else:
                                manufacturer: ReportedManufacturer = None
                            model: ReportedNetworkAdapterModel = ReportedNetworkAdapterModel(model_d.get("id") or "", model_d.get("model_name") or "", model_d.get("model") or "", model_d.get("name") or "", model_d.get("description") or "", model_d.get("status") or "", model_d.get("icon") or "", model_d.get("kind") or "", model_d.get("sku") or "", model_d.get("is_manual") if model_d.get("is_manual") else False, model_d.get("import_uuid") or "", model_d.get("updated_at") or "", model_d.get("device_type") or "", manufacturer)
                        else:
                            model: ReportedNetworkAdapterModel = None
                        network_adapters.append(ReportedNetworkAdapter(network_adapter_d.get("id") or "", network_adapter_d.get("device_id") or "", network_adapter_d.get("is_virtual") if network_adapter_d.get("is_virtual") else False, network_adapter_d.get("mac"), network_adapter_d.get("speed") or "", network_adapter_d.get("ip_address") or "", network_adapter_d.get("ipv6_address") or "", network_adapter_d.get("ip_netmask"), network_adapter_d.get("ip_prefix"), network_adapter_d.get("default") if network_adapter_d.get("default") else False, model))
                        
                else:
                    network_adapters: list[ReportedNetworkAdapter] = []
                gateways_d = osinfo_d.get("gateway") if osinfo_d.get("gateway") else None
                if gateways_d:
                    gateways: list[ReportedGateway] = []
                    for gateway_d in gateways_d:
                        gateways.append(ReportedGateway(gateway_d.get("id") or "", gateway_d.get("address")))                    
                else:
                    gateways: list[ReportedGateway] = []
                dnss_d = osinfo_d.get("dns") if osinfo_d.get("dns") else None
                if dnss_d:
                    dnss: list[ReportedDNS] = []
                    for dns_d in dnss_d:
                        dnss.append(ReportedDNS(dns_d.get("id") or "", dns_d.get("address") or ""))
                else:
                    dnss: list[ReportedDNS] = []
                domains_d = osinfo_d.get("domains") if osinfo_d.get("domains") else None
                if domains_d:
                    domains: list[ReportedDomain] = []
                    for domain_d in domains_d:
                        domains.append(ReportedDomain(domain_d.get("id") or "", domain_d.get("name") or ""))
                else:
                    domains: list[ReportedDomain] = []
                os_status_d = osinfo_d.get("osstatus") if osinfo_d.get("osstatus") else None
                if os_status_d:
                    logged_users_d = os_status_d.get("logged_users") if os_status_d.get("logged_users") else None
                    if logged_users_d:
                        logged_users: list[ReportedUser] = []
                        for user_d in logged_users_d:
                            logged_users.append(ReportedUser(user_d.get("name") or "", user_d.get("raw_username") or "", user_d.get("current") if user_d.get("current") else False, user_d.get("last_login_time") or ""))
                    else:
                        logged_users: list[ReportedUser] = []                            
                    os_status: ReportedOSStatus = ReportedOSStatus(os_status_d.get("id") or "", os_status_d.get("uptime") if os_status_d.get("uptime") else 0, os_status_d.get("boot_time") or "", os_status_d.get("firewall") or "", os_status_d.get("usb") or "", os_status_d.get("default_ip") or "", os_status_d.get("antivirus") or "", os_status_d.get("antivirus_name") or "", os_status_d.get("memory_size") if os_status_d.get("memory_size") else 0, os_status_d.get("memory_available") if os_status_d.get("memory_available") else 0, os_status_d.get("rdp_enabled") if os_status_d.get("rdp_enabled") else False, os_status_d.get("vnc_enabled") if os_status_d.get("vnc_enabled") else False, os_status_d.get("teamviewer_id") if os_status_d.get("teamviewer_id") else 0, os_status_d.get("anydesk_id") if os_status_d.get("anydesk_id") else 0, logged_users) 
                else:
                    os_status: ReportedOSStatus = None
                osinfo_set.append(ReportedOSInfo(osinfo_d.get("id") or "", osinfo_d.get("serial") or "", osinfo_d.get("product_key") or "", osinfo_d.get("hostname") or "", osinfo_d.get("azure_ad_tenant_name") or "", os, network_adapters, gateways, dnss, domains, os_status))
        else:
            osinfo_set: list[ReportedOSInfo] = None
            
        # Geolocation
        geolocation_d: dict[str, Any] = computer.get("geolocation") if computer.get("geolocation") else None
        if geolocation_d:
            geolocation: ReportedGeolocation = ReportedGeolocation(geolocation_d.get("id") or "", geolocation_d.get("latitude") if geolocation_d.get("latitude") else 0, geolocation_d.get("longitude") if geolocation_d.get("longitude") else 0)
        else:
            geolocation: ReportedGeolocation = None

        # Motherboard
        motherboard_d: dict[str, Any] = computer.get("reported_motherboard") if computer.get("reported_motherboard") else None
        if motherboard_d:
            model_d = motherboard_d.get("specs") if motherboard_d.get("specs") else None
            if model_d:
                model: ReportedMotherboardModel = ReportedMotherboardModel(model_d.get("id") or "", model_d.get("model") or "")
            else:
                model: ReportedMotherboardModel = None
            reported_motherboard: ReportedMotherboard = ReportedMotherboard(motherboard_d.get("id") or "", motherboard_d.get("serial") or "", model)
        else:
            reported_motherboard: ReportedMotherboard = None
            
        # CPU
        cpus_d: list[dict[str, Any]] = computer.get("reported_cpus") if computer.get("reported_cpus") else None
        if cpus_d:
            reported_cpus: list[ReportedCPU] = []
            for cpu_d in cpus_d:
                model_d = cpu_d.get("specs") if cpu_d.get("specs") else None
                if model_d:
                    manufacturer_d = model_d.get("manufacturer") if model_d.get("manufacturer") else None
                    if manufacturer_d:
                        manufacturer: ReportedManufacturer = ReportedManufacturer(manufacturer_d.get("id") or "", manufacturer_d.get("name") or "", manufacturer_d.get("is_manual") if manufacturer_d.get("is_manual") else False, manufacturer_d.get("is_component") if manufacturer_d.get("is_component") else False, manufacturer_d.get("logo") or "", manufacturer_d.get("support_url") or "", manufacturer_d.get("website_url") or "")
                    else:
                        manufacturer: ReportedManufacturer = None
                    model: ReportedCPUModel = ReportedCPUModel(model_d.get("id") or "", model_d.get("model_name") or "", model_d.get("model") or "", model_d.get("name") or "", model_d.get("description") or "", model_d.get("status") or "", model_d.get("icon") or "", model_d.get("kind") or "", model_d.get("sku") or "", model_d.get("is_manual") if model_d.get("is_manual") else False, model_d.get("import_uuid") or "", model_d.get("updated_at") or "", model_d.get("family") or "", model_d.get("frequency") or "", model_d.get("cores") if model_d.get("cores") else 0, manufacturer)
                else:
                    model: ReportedCPUModel = None
                reported_cpus.append(ReportedCPU(cpu_d.get("id") or "", cpu_d.get("serial") or "", cpu_d.get("created_at") or "", cpu_d.get("deleted_at") or "", cpu_d.get("assigned_cores") if cpu_d.get("assigned_cores") else 0, model))
        else:
            reported_cpus: list[ReportedCPU] = []
            
        # RAM
        rams_d: list[dict[str, Any]] = computer.get("reported_rams") if computer.get("reported_rams") else None
        if rams_d:
            reported_rams: list[ReportedRAMModule] = []
            for ram_d in rams_d:
                model_d = ram_d.get("specs") if ram_d.get("specs") else None
                if model_d:
                    manufacturer_d = model_d.get("manufacturer") if model_d.get("manufacturer") else None
                    if manufacturer_d:
                        manufacturer: ReportedManufacturer = ReportedManufacturer(manufacturer_d.get("id") or "", manufacturer_d.get("name") or "", manufacturer_d.get("is_manual") if manufacturer_d.get("is_manual") else False, manufacturer_d.get("is_component") if manufacturer_d.get("is_component") else False, manufacturer_d.get("logo") or "", manufacturer_d.get("support_url") or "", manufacturer_d.get("website_url"))
                    else:
                        manufacturer: ReportedManufacturer = None
                    model: ReportedRAMModel = ReportedRAMModel(model_d.get("id") or "", model_d.get("model_name") or "", model_d.get("model") or "", model_d.get("name") or "", model_d.get("description") or "", model_d.get("status") or "", model_d.get("icon") or "", model_d.get("kind") or "", model_d.get("sku") or "", model_d.get("is_manual") if model_d.get("is_manual") else False, model_d.get("import_uuid") or "", model_d.get("updated_at") or "", model_d.get("capacity") if model_d.get("capacity") else 0, model_d.get("speed") if model_d.get("speed") else 0, model_d.get("device_type") or "", model_d.get("width") if model_d.get("width") else 0, manufacturer)
                else:
                    model: ReportedRAMModel = None
                reported_rams.append(ReportedRAMModule(ram_d.get("id") or "", ram_d.get("bank") or "", ram_d.get("capacity") if ram_d.get("capacity") else 0, ram_d.get("speed") if ram_d.get("speed") else 0, ram_d.get("device_type") or "", ram_d.get("width") if ram_d.get("width") else 0, ram_d.get("serial") or "", ram_d.get("created_at") or "", ram_d.get("deleted_at") or "", model))
        else:
            reported_rams: list[ReportedRAMModule] = []
            
        # Storage
        storages_d: list[dict[str, Any]] = computer.get("reported_storages") if computer.get("reported_storages") else None
        if storages_d:
            reported_storages: list[ReportedStorage] = []
            for storage_d in storages_d:
                model_d = storage_d.get("specs") if storage_d.get("specs") else None
                if model_d:
                    manufacturer_d = model_d.get("manufacturer") if model_d.get("manufacturer") else None
                    if manufacturer_d:
                        manufacturer: ReportedManufacturer = ReportedManufacturer(manufacturer_d.get("id") or "", manufacturer_d.get("name") or "", manufacturer_d.get("is_manual") if manufacturer_d.get("is_manual") else False, manufacturer_d.get("is_component") if manufacturer_d.get("is_component") else False, manufacturer_d.get("logo") or "", manufacturer_d.get("support_url") or "", manufacturer_d.get("website_url") or "")
                    else:
                        manufacturer: ReportedManufacturer = None
                    model: ReportedStorageModel = ReportedStorageModel(model_d.get("id") or "", model_d.get("model_name") or "", model_d.get("model") or "", model_d.get("name") or "", model_d.get("description") or "", model_d.get("status") or "", model_d.get("icon") or "", model_d.get("kind") or "", model_d.get("sku") or "", model_d.get("is_manual") if model_d.get("is_manual") else False, model_d.get("import_uuid") or "", model_d.get("updated_at") or "", model_d.get("device_type") or "", model_d.get("disk_type") or "", manufacturer)    
                else:
                    model: ReportedStorageModel = None
            reported_storages.append(ReportedStorage(storage_d.get("id") or "", storage_d.get("created_at") or "", storage_d.get("deleted_at"), storage_d.get("capacity") if storage_d.get("capacity") else 0, storage_d.get("label") or "", storage_d.get("available") if storage_d.get("available") else 0, model))
        else:
            reported_storages: list[ReportedStorage] = []
        # Printer
        printers_d: list[dict[str, Any]] = computer.get("reported_printers") if computer.get("reported_printers") else None
        if printers_d:
            reported_printers: list[ReportedPrinter] = []
            for printer_d in printers_d:
                model_d = printer_d.get("specs") if printer_d.get("specs") else None
                if model_d:
                    manufacturer_d = model_d.get("manufacturer") if model_d.get("manufacturer") else None
                    if manufacturer_d:
                        manufacturer: ReportedManufacturer = ReportedManufacturer(manufacturer_d.get("id") or "", manufacturer_d.get("name") or "", manufacturer_d.get("is_manual") if manufacturer_d.get("is_manual") else False, manufacturer_d.get("is_component") if manufacturer_d.get("is_component") else False, manufacturer_d.get("logo") or "", manufacturer_d.get("support_url") or "", manufacturer_d.get("website_url") or "")
                    else:
                        manufacturer: ReportedManufacturer = None
                    model: ReportedPrinterModel = ReportedPrinterModel(model_d.get("id") or "", model_d.get("model_name") or "", model_d.get("model") or "", model_d.get("name") or "", model_d.get("description") or "", model_d.get("status") or "", model_d.get("icon") or "", model_d.get("kind") or "", model_d.get("sku") or "", model_d.get("is_manual") if model_d.get("is_manual") else False, model_d.get("import_uuid") or "", model_d.get("updated_at") or "", manufacturer)
                else:
                    model: ReportedPrinterModel = None
                reported_printers.append(ReportedPrinter(printer_d.get("id") or "", printer_d.get("created_at") or "", printer_d.get("deleted_at") or "", model))
        else:
            reported_printers: list[ReportedPrinter] = []
        
        # Monitor
        monitors_d: list[dict[str, Any]] = computer.get("reported_monitors") if computer.get("reported_monitors") else None
        if monitors_d:
            reported_monitors: list[ReportedMonitor] = []
            for monitor_d in monitors_d:
                model_d = monitor_d.get("specs") if monitor_d.get("specs") else None
                if model_d:
                    manufacturer_d = model_d.get("manufacturer") if model_d.get("manufacturer") else None
                    if manufacturer_d:
                        manufacturer: ReportedManufacturer = ReportedManufacturer(manufacturer_d.get("id") or "", manufacturer_d.get("name") or "", manufacturer_d.get("is_manual") if manufacturer_d.get("is_manual") else False, manufacturer_d.get("is_component") if manufacturer_d.get("is_component") else False, manufacturer_d.get("logo") or "", manufacturer_d.get("support_url") or "", manufacturer_d.get("website_url") or "")
                    else:
                        manufacturer: ReportedManufacturer = None
                    model: ReportedMonitorModel = ReportedMonitorModel(model_d.get("id") or "", model_d.get("model_name") or "", model_d.get("model") or "", model_d.get("height_measurement_unit") or "", model_d.get("width_measurement_unit") or "", model_d.get("diagonal_measurement_unit") or "", model_d.get("name") or "", model_d.get("description") or "", model_d.get("status") or "", model_d.get("icon") or "", model_d.get("kind") or "", model_d.get("sku") or "", model_d.get("is_manual") if model_d.get("is_manual") else False, model_d.get("import_uuid") or "", model_d.get("updated_at") or "", model_d.get("height") if model_d.get("height") else 0, model_d.get("width") if model_d.get("width") else 0, model_d.get("ratio") if model_d.get("ratio") else 0, model_d.get("diagonal") if model_d.get("diagonal") else 0, model_d.get("resolution") or "", manufacturer)
                else:
                    model: ReportedMonitorModel = None
                reported_monitors.append(ReportedMonitor(monitor_d.get("id") or "", monitor_d.get("created_at") or "", monitor_d.get("deleted_at") or "", monitor_d.get("edid") or "", monitor_d.get("serial") or "", model))
        else:
            reported_monitors: list[ReportedMonitor] = []
        
        # BIOS
        bios_d: dict[str, Any] = computer.get("reported_bios") if computer.get("reported_bios") else None
        if bios_d:
            reported_bios: ReportedBIOS = ReportedBIOS(bios_d.get("id") or "", bios_d.get("date") or "", bios_d.get("version") or "")
        else:
            reported_bios: ReportedBIOS = None
            
        return InvgateComputer(computer.get("id") or "", asset, computer.get("total_ram") if computer.get("total_ram") else 0, computer.get("format_type") or "", computer.get("name") or "", computer.get("inventory_id") or "", computer.get("serial") or "", computer.get("virtual") or "", computer.get("firewall_status") or "",computer.get("antivirus_status") or "", computer.get("connectivity_status") or "", computer.get("last_logged_user") or "", osinfo_set, geolocation, reported_motherboard, reported_cpus, reported_rams, reported_storages, reported_printers, reported_monitors, reported_bios)
        
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

    def map_included_data(self, included_data: list[dict]) -> dict[str, dict[str, Any]]:
        if not included_data: 
            return None
        mapped_data: dict[str, dict[str, Any]] = {}
        for data in included_data:
            if data.get("type") and data.get("id"):
                if not mapped_data.get(data.get("type")):
                    mapped_data[data.get("type")] = {}
                mapped_data[data.get("type")][data.get("id")] = data
            else:
                continue
        return mapped_data
    
    def flatten_data(self, mapped_data: dict[str, dict[str, Any]], obj: dict[str, Any], parents: list = None):
        parents = parents or []
        if mapped_data and obj:
            if obj.get("type") and obj.get("id") and {obj.get("type"): obj.get("id")} in parents:
                return None
            flattened_data: dict[str, Any] = {}
            flattened_data["type"] = obj.get("type")
            flattened_data["id"] = obj.get("id")
            if obj.get("attributes"):
                for key, value in obj.get("attributes").items():
                    flattened_data[key] = value
            if obj.get("relationships"):
                for key, value in obj.get("relationships").items():
                    if isinstance(value.get("data"), list):
                        flattened_data[key] = []
                        for item in value.get("data"):
                            matched_data = mapped_data.get(item.get("type")).get(item.get("id")) if item.get("type") and item.get("id") and mapped_data.get(item.get("type")) and mapped_data.get(item.get("type")).get(item.get("id")) and {item.get("type"): item.get("id")} not in parents else None
                            if matched_data:
                                next_parents = parents + [{obj.get("type"): obj.get("id")}]
                                flattened_data[key].append(self.flatten_data(mapped_data, matched_data, next_parents))
                    else:
                        matched_data = mapped_data.get(value.get("data").get("type")).get(value.get("data").get("id")) if value.get("data") and value.get("data").get("type") and value.get("data").get("id") and mapped_data.get(value.get("data").get("type")) and mapped_data.get(value.get("data").get("type")).get(value.get("data").get("id")) and {value.get("data").get("type"): value.get("data").get("id")} not in parents else None
                        if matched_data:
                            next_parents = parents + [{obj.get("type"): obj.get("id")}]
                            flattened_data[key] = self.flatten_data(mapped_data, matched_data, next_parents)
            return flattened_data
        return None
        
        