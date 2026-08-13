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

class InvgateConnection:
    """
    A class for connecting, extracting, and uploading data to and from the Invgate API.
    """
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
    def get_data(self, endpoint_path: str = None, page: str = None, v1: bool = False, query: str = None, full_path: str = None):
        """
        Makes a GET request to the API using the authenticated session.
        
        Arguments:
            endpoint_path (str): The part of the URL after the base URL. Specifies which API route to access. Ignored if full_path is also provided.
            page (str): The page to get data from. Used when accessing paginated data.
            v1 (bool): Refers to the version of the Invgate API. The default API version used is version 2. Set v1 to True to access certain routes that are unavailable in version 2 at the moment.
            query (str): Specifies query parameters to include in the GET request. Parameters should be separated by & and not contain any spaces. E.g. id=10&name=john.
            full_path (str): The full URL. This is used interchangeably with endpoint_path. endpoint_path will be ignored if this value is provided.

        Returns:
            Dictionary (dict): If results are found, returns a dict object.
            None: If authentication failed or GET request failed.

        Raises:
            RequestException: If the GET request failed.
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
            full_url = f"{self.domain}{endpoint_path}"
            if page and query:
                full_url = full_url + f"?page={page}&{query}"
            elif page:
                full_url = full_url + f"?page={page}"
            elif query:
                full_url = full_url + f"?{query}"

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
    
    def patch_data(self, endpoint_path, payload):
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

    def get_user(self, id: int = None, name: str = None, email: str = None, employee_id: str = None, user_username: str = None) -> InvgateUser:
        """
        Gets a single user from Invgate and returns an InvgateUser object.

        Arguments:
            id* (int): The unique identifier of the user to get from Invgate.

        Returns:
            InvgateUser: If user is found.
            None: If user is not found.
        """

        if not self.validate_parameters(id, name, email, employee_id, user_username):
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

            location: InvgateLocation = self.get_location(id = self.get("location")) if user.get("location") else None

            return InvgateUser(user.get("id") if user.get("id") else 0, user.get("name") or "", user.get("email") or "", user.get("date_of_birth") or "", user.get("employee_id") or "", user.get("position") or "", user.get("department") or "", user.get("company") or "", user.get("phone") or "", user.get("cellphone") or "", user.get("address") or "", user.get("person_type") or "", user_id, username, manager_id, manager_name, manager_email, location, user.get("cost_center") or "")
        print("Get User failed: User not found or invalid response received.")
        return None

    def get_finance(self, id: int) -> InvgateFinance:
        """
            Gets a single finance from Invgate and returns an InvgateFinance object.
        
            Arguments:
                id* (int): The unique identifier of the finance to get from Invgate.
        
            Returns:
                InvgateFinance: If finance is found.
                None: If finance is not found.
        """        
        response = self.get_data(endpoint_path = routes.financial(id))
        if response:
            vendor = self.get_vendor(response.get("supplier")) if response.get("supplier") else None
            purchase_order = self.get_purchase_order(response.get("order_id")) if response.get("order_id") else None
            return InvgateFinance(response.get("id") if response.get("id") else 0, response.get("asset") if response.get("asset") else 0, response.get("acquisition_type") or "", response.get("acquisition_date") or "", response.get("acquisition_price") if response.get("acquisition_price") else 0, response.get("actual_price") if response.get("actual_price") else 0, response.get("depreciation_percentage") if response.get("depreciation_percentage") else 0, response.get("residual_value") if response.get("residual_value") else 0, response.get("warranty_date") or "", vendor, response.get("cost_center") or "", purchase_order, response.get("invoice_id") or "")
            
        print("Get Finance failed: Finance not found or invalid response received.")
        return None

    def get_vendor(self, id: int) -> InvgateVendor:
        """
        Gets a single vendor from Invgate and returns an InvgateVendor object.

        Arguments:
            id* (int): The unique identifier of the vendor to get from Invgate.

        Returns:
            InvgateVendor: If vendor is found.
            None: If vendor is not found.
        """        
        response = self.get_data(endpoint_path = routes.vendor(id))
        if response:
            return InvgateVendor(response.get("id") if response.get("id") else 0, response.get("company_name") or "", response.get("legal_name") or "", response.get("status") or "", response.get("country") or "", response.get("website") or "", response.get("address") or "", response.get("email") or "", response.get("billing_currency") or "", response.get("phone") or "", response.get("industry") or "")
        return None

    def get_tag(self, id: int = None, name: str = None) -> InvgateTag:
        """
        Gets a single tag from Invgate and returns an InvgateTag object.

        Arguments:
            id* (int): The unique identifier of the tag to get from Invgate.

        Returns:
            InvgateTag: If tag is found.
            None: If tag is not found.
        """
        if not self.validate_parameters(id, name):
            print("Get Tag failed: Please provide one field to get a tag by.")
            return None
        query = ""
        if id:
            query = f"tag_ids={id}"
        elif name:
            query = f"name={name}"

        response = self.get_data(endpoint_path = routes.tags(), query = query)
        tag = response.get("results")[0]
        if response and response.get("results") and len(response.get("results")) == 1:
            return InvgateTag(tag.get("id") if tag.get("id") else 0, tag.get("name") or "", tag.get("color") or "", tag.get("description") or "", tag.get("smart_tag") if tag.get("smart_tag") else False, tag.get("locked") if tag.get("locked") else False)
        print("Get Tag failed: Tag not found or invalid response received.")
        return None

    def get_purchase_order(self, id: int, order_number: str) -> InvgatePurchaseOrder:
        """
        Gets a single purchase order from Invgate and returns an InvgatePurchaseOrder object.

        Arguments:
            id* (int): The unique identifier of the purchase to get from Invgate.

        Returns:
            InvgatePurchaseOrder: If purchase order is found.
            None: If purchase order is not found.
        """
        if not self.validate_parameters(id, order_number):
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
        vendor = self.get_vendor(po.get("vendor")) if po.get("vendor") else None
        return InvgatePurchaseOrder(po.get("id") if po.get("id") else 0, po.get("order_number") or "", vendor, po.get("purchase_order_type") or "", po.get("creation_date") or "", po.get("expected_delivery_date") or "", po.get("date_delivered") or "", po.get("ship_method") or "", po.get("billing_address") or "", po.get("status") or "", po.get("subtotal") if po.get("subtotal") else 0, po.get("freight") or "", po.get("handling") or "", po.get("tax") if po.get("tax") else 0, po.get("total_cost") if po.get("total_cost") else 0, po.get("cost_center") or "", po.get("contract") or "")

    def get_manufacturer(self, id: int = None, name: str = None) -> InvgateManufacturer:
        """
        Gets a single manufacturer from Invgate and returns an InvgateManufacturer object.

        Arguments:
            id (int): The unique identifier of the manufacturer to get from Invgate.
            name (str): The name of the manufacturer to get from Invgate.

        Returns:
            InvgateManufacturer: If manufacturer is found.
            None: If manufacturer is not found.
        """
        if not self.validate_parameters(id, name):
            print("Get Manufacturer failed: Please provide one field to get a manufacturer by.")
            return None

        query: str = ""
        if id:
            query = f"ids={id}"
        elif name:
            query = f"name={name}"

        response = self.get_data(endpoint_path = routes.manufacturers, query = query)
        if response and response.get("results") and len(response.get("results") == 1):
            manufacturer = response.get("results")[0]
            return InvgateManufacturer(manufacturer.get("id") if manufacturer.get("id") else 0, manufacturer.get("name") or "")
        print("Get Manufacturer failed: Manufacturer not found or invalid response received.")
        return None

    def get_health(self, computer_id: int) -> InvgateHealth:
        """
        Gets a single health from Invgate and returns an InvgateHealth object.

        Arguments:
            computer_id* (int): The unique identifier of the asset to which the health belongs.

        Returns:
            InvgateHealth: If health is found.
            None: If health is not found.
        """
        response = self.get_data(endpoint_path = routes.health(computer_id))
        if response:
            return InvgateHealth(response.get("id") if response.get("id") else 0, response.get("updated_at") or "", response.get("health_rule") or "", response.get("status") or "")
        print("Get Health failed: Health not found or invalid response received.")
        return None

    def get_status(self, id: int = None, name: str = None) -> InvgateStatus:
        """
        Gets a single status from Invgate and returns an InvgateStatus object.

        Arguments:
            id* (int): The unique identifier of the status to get from Invgate.

        Returns:
            InvgateStatus: If status is found.
            None: If status is not found.
        """
        if not self.validate_parameters(id, name):
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
        """
        Gets a single location from Invgate and returns an InvgateLocation object.

        Arguments:
            id* (int): The unique identifier of the location to get from Invgate.

        Returns:
            InvgateLocation: If location is found.
            None: If location is not found.
        """
        if not self.validate_parameters(id, name):
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
        """
        Gets a single software from Invgate and returns an InvgateSoftware object.

        Arguments:
            id* (int): The unique identifier of the software to get from Invgate.

        Returns:
            InvgateSoftware: If software is found.
            None: If software is not found.
        """
        response = self.get_data(endpoint_path = routes.software(id))
        if response:
            manufacturer: InvgateManufacturer = InvgateManufacturer(response.get("version").get("program").get("manufacturer").get("id"), response.get("version").get("program").get("manufacturer").get("name") or "") if response.get("version") and response.get("version").get("program") and response.get("version").get("program").get("manufacturer") else None
            program: InvgateProgram = InvgateProgram(response.get("version").get("program").get("name") or "", response.get("version").get("program").get("license") or "", response.get("version").get("program").get("category") or "", response.get("version").get("program").get("types") or "", response.get("version").get("program").get("types_key") or "", response.get("version").get("program").get("tags") or "", response.get("version").get("program").get("is_metering_enabled"), manufacturer) if response.get("version") and response.get("version").get("program") else None
            version: InvgateVersion = InvgateVersion(response.get("version").get("version") or "", response.get("version").get("internal_version") or "", response.get("version").get("edition") or "", program) if response.get("version") else None
            return InvgateSoftware(response.get("id") if response.get("id") else 0, response.get("resource_type") or "", response.get("install_date") or "", response.get("install_path") or "", response.get("uninstall_call") or "", response.get("computer") if response.get("computer") else 0, version) if response.get("version") and response.get("version").get("program") and response.get("version").get("program").get("manufacturer") else None
        print("Get Software failed: Software not found or invalid response received.")

    def get_asset(self, id: int = None, name: str = None, serial: str = None) -> InvgateAsset:
        """
        Gets a single asset from Invgate and returns an InvgateAsset object.
        
        Arguments:
            id (int): The unique identifier of the asset to get from Invgate.
            name (str): The name of the asset to get from Invgate.

        Returns:
            InvgateAsset: If asset is found.
            None: If asset is not found.
        """
        if not self.validate_parameters(id, name, serial):
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
        """
        Gets a single operating system update from Invgate and returns an InvgateOperatingSystemUpdate object.

        Arguments:
            id* (int): The unique identifier of the operating system update to get from Invgate.

        Returns:
            InvgateOperatingSystemUpdate: If operating system update is found.
            None: If operating system update is not found.
        """
        response = self.get_data(endpoint_path = routes.operating_system_update(id))
        if response:
            os_update: InvgateOperatingSystemUpdate = InvgateOperatingSystemUpdate(response.get("os_update_version").get("os_update").get("short_name") or "", response.get("os_update_version").get("os_update").get("name") or "", response.get("os_update_version").get("os_update").get("update_type") or "", response.get("os_update_version").get("os_update").get("os_type") or "", response.get("os_update_version").get("os_update").get("severity") or "", response.get("os_update_version").get("os_update").get("support_url") or "") if response.get("os_update_version") and response.get("os_update_version").get("os_update") else None
            os_update_version: InvgateOperatingSystemUpdateVersion = InvgateOperatingSystemUpdateVersion(response.get("os_update_version").get("version") or "", response.get("os_update_version").get("release_date") or "", os_update) if response.get("os_update_version") else None
            return InvgateUpdate(response.get("id") if response.get("id") else 0, response.get("install_date") or "", response.get("status") or "", response.get("computer") if response.get("computer") else 0, os_update_version)
        print("Get Update Failed: Update not found or invalid response received.")
        return None

    def get_updates_for_computer(self, computer_id: int) -> dict:
        """
        Gets all operating system updates that belong to the specified asset id and returns them as InvgateOperatingSystemUpdate objects
        Arguments:
            computer_id* (int): The unique identifier of the asset that the operating system updates belong to. 
        Returns:
            dict[int, list[InvgateOperatingSystemUpdate]]: If operating system updates are found.
            None: If no operating system updates are found.
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


    def get_software_for_computer(self, computer_id: int) -> list:
        """
        Gets software installations that belong to the specified asset id and returns them as InvgateSoftware objects
        Arguments:
            computer_id* (int): The unique identifier of the asset that the software installations belong to. 
        Returns:
            dict[int, list[InvgateSoftware]]: If software installations are found.
            None: If no software installations are found.
        """
        response = self.get_all_pages(self.get_data(endpoint_path = routes.manufacturers()))
        manufacturers: dict[InvgateManufacturer] = {}
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
                manufacturer: InvgateManufacturer = manufacturers.get(software.get("version").get("program").get("manufacturer").get("id")) if software.get("version") and software.get("version").get("program") and software.get("version").get("program").get("manufacturer") and manufacturers.get(software.get("version").get("program").get("manufacturer")) else None
                program: InvgateProgram = InvgateProgram(software.get("version").get("program").get("name") or "", software.get("version").get("program").get("license") or "", software.get("version").get("program").get("category") or "", software.get("version").get("program").get("types") or "", software.get("version").get("program").get("types_key") or "", software.get("version").get("program").get("tags") or "", software.get("version").get("program").get("is_metering_enabled"), manufacturer) if software.get("version") and software.get("version").get("program") else None
                version: InvgateVersion = InvgateVersion(software.get("version").get("version") or "", software.get("version").get("internal_version") or "", software.get("version").get("edition") or "", program) if software.get("version") else None
            return InvgateSoftware(software.get("id") if software.get("id") else 0, software.get("resource_type") or "", software.get("install_date") or "", software.get("install_path") or "", software.get("uninstall_call") or "", software.get("computer") if software.get("computer") else 0, version) if software.get("version") and software.get("version").get("program") and software.get("version").get("program").get("manufacturer") else None

    def get_asset_with_collections(self, id: int = None, name: str = None, serial: str = None) -> InvgateAsset:
        """
        Gets a single asset from Invgate along with its collections and returns an InvgateAsset object.
        
        Arguments:
            id (int): The unique identifier of the asset to get from Invgate.
            name (str): The name of the asset to get from Invgate.

        Returns:
            InvgateAsset: If asset is found.
            None: If asset is not found.
        """
        if not self.validate_parameters(id, name, serial):
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
            asset_object.populate_collections(health = health, software = software, updates = updates)
        print("Get Asset failed: Asset not found or invalid response received.")
        return None
                
    def load_data(self) -> dict:

        results = {}

        # Vendors
        temp_vendors = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.vendors()))
        for vendor in response.get("data"):
            temp_vendors[vendor.get("id")] = InvgateVendor(vendor.get("id") if vendor.get("id") else 0, vendor.get("company_name") or "", vendor.get("legal_name") or "", vendor.get("status") or "", vendor.get("tax_id") or "", vendor.get("country") or "", vendor.get("website") or "", vendor.get("address") or "", vendor.get("email") or "", vendor.get("billing_currency") or "", vendor.get("phone") or "", vendor.get("industry") or "")

        # Manufacturers
        temp_manufacturers = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.manufacturers()))
        for manufacturer in response.get("data"):
            temp_manufacturers[manufacturer.get("name")] = InvgateManufacturer(manufacturer.get("id") if manufacturer.get("id") else 0, manufacturer.get("name") or "")

        # Locations
        temp_locations = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.locations(), v1 = True))
        for location in response.get("data"):
            temp_locations[location.get("id")] = InvgateLocation(location.get("id") if location.get("id") else 0, location.get("attributes").get("name") or "", location.get("attributes").get("full_path") or "", location.get("attributes").get("description") or "", location.get("attributes").get("content_type") or "")
        # Statuses
        temp_statuses = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.status(), v1 = True))
        for status in response.get("data"):
            temp_statuses[status.get("id")] = InvgateStatus(status.get("id") if status.get("id") else 0, status.get("attributes").get("name") or "", status.get("attributes").get("description") or "", status.get("attributes").get("behavior") or "", status.get("attributes").get("is_default") if status.get("attributes").get("is_default") else False)
        # Purchase Orders
        temp_purchase_orders = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.purchase_orders()))
        for po in response.get("data"):
            vendor = temp_vendors.get(po.get("vendor")) if po.get("vendor") else None
            temp_purchase_orders[po.get("order_number")] = InvgatePurchaseOrder(po.get("id") if po.get("id") else 0, po.get("order_number") or "", vendor, po.get("purchase_order_type") or "", po.get("creation_date") or "", po.get("expected_delivery_date") or "", po.get("date_delivered") or "", po.get("ship_method") or "", po.get("billing_address") or "", po.get("status") or "", po.get("subtotal") if po.get("subtotal") else 0, po.get("freight") or "", po.get("handling") or "", po.get("tax") if po.get("tax") else 0, po.get("total_cost") if po.get("total_cost") else 0, po.get("cost_center") or "", po.get("contract") or "")
        # Finance
        temp_finance = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.financials()))
        for finance in response.get("data"):
            vendor = temp_vendors.get(finance.get("vendor")) if finance.get("vendor") else None
            purchase_order = temp_purchase_orders.get(finance.get("order_id")) if finance.get("order_id") else None

            temp_finance[finance.get("id")] = InvgateFinance(finance.get("id") if finance.get("id") else 0, finance.get("asset") if finance.get("asset") else 0, finance.get("acquisition_type") or "", finance.get("acquisition_date") or "", finance.get("acquisition_price") if finance.get("acquisition_price") else 0, finance.get("actual_price") if finance.get("actual_price") else 0, finance.get("depreciation_percentage") if finance.get("depreciation_percentage") else 0, finance.get("residual_value") if finance.get("residual_value") else 0, finance.get("warranty_date") or "", vendor, finance.get("cost_center") or "", purchase_order, finance.get("invoice_id") or "")

        # Users
        response = self.get_all_pages(self.get_data(endpoint_path = routes.users_detail()))
        temp_users = {}
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
                user_id = user.get("id")
                username = user.get("username")
                

            location = temp_locations.get(user.get("location").get("id")) if user.get("location") and user.get("location").get("id") else None
            user_object = InvgateUser(user.get("id") if user.get("id") else 0, user.get("name") or "", user.get("email") or "", user.get("date_of_birth") or "", user.get("employee_id") or "", user.get("position") or "", user.get("department") or "", user.get("company") or "", user.get("phone") or "", user.get("cellphone") or "", user.get("address") or "", user.get("person_type") or "", user_id, username, manager_id, manager_name, manager_email, location, user.get("cost_center") or "")
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
        """
        Creates a new asset in Invgate using the data from an InvgateAsset object.
        
        Arguments:
            asset* (InvgateAsset): The InvgateAsset object to create in Invgate.

        Returns:
            InvgateAsset: If asset is created successfully.
            None: If asset is not created successfully.
        """
        response = self.post_data(endpoint_path = routes.assets(), payload = asset.to_json())

        if response["id"]:
            if response["status"]:
                status = self.get_status(id = response.get("status"))
            else:
                status = None

            if response["location"]:
                location = self.get_location(id = response.get("location"))
            else:
                location = None

            if response["owner"]:
                owner = self.get_user(id = response.get("owner"))
            else:
                owner = None

            if response["finance"]:
                finance = self.get_finance(id = response.get("finance"))
            else:
                finance = None

            if response["manufacturer"]:
                manufacturer = self.get_manufacturer(name = response.get("manufacturer"))
            else:
                manufacturer = None

            return InvgateAsset(name = response.get("name"), id = response.get("id"), serial = response.get("serial"), inventory_id = response.get("inventory_id"), asset_physical_tag = response.get("asset_physical_tag"), created_at = response.get("created_at"), reported_at = response.get("reported_at"), updated_at = response.get("updated_at"), status = status, location = location, owner = owner, finance = finance, manufacturer = manufacturer, model = response.get("model"), commercial_model = response.get("commercial_model"), asset_type = response.get("asset_type"), default_ip = response.get("default_ip"), mac_address = response.get("mac_address"), asset_type_code = response.get("asset_type_code"), format = response.get("format"))

    def create_user(self, user: InvgateUser) -> InvgateUser:
        """
        Creates a new user in Invgate using the data from an InvgateUser object.
        
        Arguments:
            user* (InvgateUser): The InvgateUser object to create in Invgate.

        Returns:
            InvgateUser: If user is created successfully.
            None: If user is not created successfully.
        """
        response = self.post_data(endpoint_path = routes.users(), payload = user.to_json())

        if response["id"]:
            if response["manager"]:
                manager = self.get_user(id = response.get("manager"))
            else:
                manager = None

            if response["location"]:
                location = self.get_location(id = response.get("location"))
            else:
                location = None

            return InvgateUser(id = response.get("id"), name = response.get("name"), email = response.get("email"), date_of_birth = response.get("date_of_birth"), employee_id = response.get("employee_id"), position = response.get("position"), department = response.get("department"), company = response.get("company"), phone = response.get("phone"), cellphone = response.get("cellphone"), address = response.get("address"), person_type = response.get("person_type"), user = response.get("user"), manager = manager, location = location, cost_center = response.get("cost_center"))
        print(response)
        return None

    # ==================================================================================================
    # Update Methods: Methods to export data from Python objects and update existing objects in Invgate.
    # ==================================================================================================

    def update_asset(self, asset: InvgateAsset) -> InvgateAsset:
        """
        Updates an existing asset in Invgate using the data from an InvgateAsset object.
        
        Arguments:
            asset* (InvgateAsset): The InvgateAsset object to update in Invgate.
            
        Returns:
            InvgateAsset: If asset is updated successfully.
            None: If asset is not updated successfully.    
        """
        response = self.patch_data(endpoint_path = routes.asset(asset.id), payload = asset.to_json())

        if response["id"]:
            if response["status"]:
                status = self.get_status(id = response.get("status"))
            else:
                status = None

            if response["location"]:
                location = self.get_location(id = response.get("location"))
            else:
                location = None

            if response["owner"]:
                owner = self.get_user(id = response.get("owner"))
            else:
                owner = None

            if response["finance"]:
                finance = self.get_finance(id = response.get("finance"))
            else:
                finance = None

            if response["manufacturer"]:
                manufacturer = self.get_manufacturer(name = response.get("manufacturer"))
            else:
                manufacturer = None

            return InvgateAsset(name = response.get("name"), id = response.get("id"), serial = response.get("serial"), inventory_id = response.get("inventory_id"), asset_physical_tag = response.get("asset_physical_tag"), created_at = response.get("created_at"), reported_at = response.get("reported_at"), updated_at = response.get("updated_at"), status = status, location = location, owner = owner, finance = finance, manufacturer = manufacturer, model = response.get("model"), commercial_model = response.get("commercial_model"), asset_type = response.get("asset_type"), default_ip = response.get("default_ip"), mac_address = response.get("mac_address"), asset_type_code = response.get("asset_type_code"), format = response.get("format"))
        else:
            print(response)
            return None

    def update_user(self, user: InvgateUser) -> InvgateUser:
        """
        Updates an existing user in Invgate using the data from an InvgateUser object.

        Arguments:
            user* (InvgateUser): The InvgateUser object to update in Invgate.

        Returns:
            InvgateUser: If user is updated successfully.
            None: If user is not updated successfully.
        """
        response = self.patch_data(endpoint_path = routes.user(user.id), payload = user.to_json())

        if response["id"]:
            if response["manager"]:
                manager = self.get_user(id = response.get("manager"))
            else:
                manager = None

            if response["location"]:
                location = self.get_location(id = response.get("location"))
            else:
                location = None

            return InvgateUser(name = response.get("name"), email = response.get("email"), id = response.get("id"), date_of_birth = response.get("date_of_birth"), employee_id = response.get("employee_id"), position = response.get("position"), department = response.get("department"), company = response.get("company"), phone = response.get("phone"), cellphone = response.get("cellphone"), address = response.get("address"), person_type = response.get("person_type"), user = response.get("user"), manager = manager, location = location, cost_center = response.get("cost_center"))
        else:
            print(response)
            return None

# ================================================
# Helper Functions
# ================================================
    def get_all_pages(self, response: dict) -> dict:
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
            elif response.get("data"):
                results["count"] = len(response.get("data"))
                while True:
                    results["data"].extend(response.get("data"))

                    if not response.get("links").get("next"):
                        break
                    elif response.get("next") == "None":
                        break
                    else:
                        response = self.get_data(full_path = response.get("next"))
            else:
                return response

            return results
        else:
            return None

    def validate_parameters(parameters: list) -> bool:
        count_parameters: int = 0
        for parameter in parameters:
            if parameter:
                count_parameters += 1

        if count_parameters != 1:
            return False
        return True