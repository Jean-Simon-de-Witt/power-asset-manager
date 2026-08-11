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
from classes.invgate.invgate_software import InvgateSoftware
from classes.invgate.invgate_operating_system_update import InvgateOperatingSystemUpdate
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
        parameter_count = 0
        for parameter in [id, name, email, employee_id, user_username]:
            if parameter:
                parameter_count += 1

        if parameter_count < 1:
            print("Get User failed: Please provide a field to fetch the user by.")
            return None
        elif parameter_count > 1:
            print("Get User failed: Please provide only one field to fetch the user by.")
            return None
        else:
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

            response = self.get_data(endpoint_path = routes.users_detail, query = query)
        
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

                location: InvgateLocation = self.get_location(self.get("location")) if user.get("location") else None

                return InvgateUser(user.get("id") if user.get("id") else 0, user.get("name") or "", user.get("email") or "", user.get("date_of_birth") or "", user.get("employee_id") or "", user.get("position") or "", user.get("department") or "", user.get("company") or "", user.get("phone") or "", user.get("cellphone") or "", user.get("address") or "", user.get("person_type") or "", user_id, username, manager_id, manager_name, manager_email, location, user.get("cost_center") or "")
            else:
                return None

    # Gets a single finance from Invgate and returns an InvgateFinance object.
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
            if response["supplier"]:
                vendor = self.get_vendor(response.get("supplier"))
            else:
                vendor = None

            if response["order_id"]:
                purchase_order = self.get_purchase_order_by_order_id(response.get("order_id"))
            else:
                purchase_order = None
            return InvgateFinance(id = response.get("id"), asset = response.get("asset"), acquisition_type = response.get("acquisition_type"), acquisition_date = response.get("acquisition_date"), acquisition_price = response.get("acquisition_price"), actual_price = response.get("actual_price"), residual_value = response.get("residual_value"), depreciation_percentage = response.get("depreciation_percentage"), warranty_date = response.get("warranty_date"), vendor = vendor, cost_center = response.get("cost_center"), purchase_order = purchase_order, invoice_id = response.get("invoice_id"))
        return None

    def get_finances(self, page: str = None) -> dict:
        """
        Gets all finances on the specified page from Invgate and returns the count, previous page, next page, and a list of InvgateFinance objects. If no page is specified, returns data from the first page.
        Arguments:
            page (str): Specifies which page to get data from. If it's not specified, data will be accessed from the first page.
        
        Returns:
            dict[int, str, str, list[InvgateFinance]]: If finances are found, there is a previous URL, and a next URL.
            dict[int, str, list[InvgateFinance]]: If finances are found, there is a previous URL, or a new URL.
            dict[int, list[InvgateFinance]]: If finances are found.
            None: If no finances are found.
        """
        if page:
            response = self.get_data(endpoint_path = routes.financials(), page = page)
        else:
            response = self.get_data(endpoint_path = routes.financials())

        if response and response["results"]:
            results = {"count": response.get("count")}

            if response["next"]:
                results["next"] = response.get("next")

            if response["previous"]:
                results["previous"] = response.get("previous")

            finances = response.get("results")
            results["finances"] = []

            for f in finances:
                if f["supplier"]:
                    vendor = self.get_vendor(f.get("supplier"))
                else:
                    vendor = None

                if f["order_id"]:
                    purchase_order = self.get_purchase_order_by_order_id(f.get("order_id"))
                else:
                    purchase_order = None
                results["finances"].append(InvgateFinance(id = f.get("id"), asset = f.get("asset"), acquisition_type = f.get("acquisition_type"), acquisition_date = f.get("acquisition_date"), acquisition_price = f.get("acquisition_price"), actual_price = f.get("actual_price"), residual_value = f.get("residual_value"), depreciation_percentage = f.get("depreciation_percentage"), warranty_date = f.get("warranty_date"), vendor = vendor, cost_center = f.get("cost_center"), purchase_order = purchase_order, invoice_id = f.get("invoice_id")))
            return results
        else:
            print("No results.")
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
            return InvgateVendor(company_name = response.get("company_name"), id = response.get("id"), legal_name = response.get("legal_name"), status = response.get("status"), country = response.get("country"), address = response.get("address"), email = response.get("email"), billing_currency = response.get("billing_currency"), phone = response.get("phone"), industry = response.get("industry"))
        return None

    def get_vendors(self, page: str = None) -> dict:
        """
        Gets all vendors on the specified page from Invgate and returns the count, previous page, next page, and a list of InvgateVendor objects. If no page is specified, returns data from the first page.
        Arguments:
            page (str): Specifies which page to get data from. If it's not specified, data will be accessed from the first page.
        
        Returns:
            dict[int, str, str, list[InvgateVendor]]: If vendors are found, there is a previous URL, and a next URL.
            dict[int, str, list[InvgateVendor]]: If vendors are found, there is a previous URL, or a new URL.
            dict[int, list[InvgateVendor]]: If vendors are found.
            None: If no vendors are found.
        """
        if page:
            response = self.get_data(endpoint_path = routes.vendors(), page = page)
        else:
            response = self.get_data(endpoint_path = routes.vendors())

        if response and response["results"]:
            results = {"count": response.get("count")}

            if response["next"]:
                results["next"] = response.get("next")

            if response["previous"]:
                results["previous"] = response.get("previous")

            vendors = response.get("results")
            results["vendors"] = []

            for v in vendors:
                results["vendors"].append(InvgateVendor(id = v.get("id"), company_name = v.get("company_name"), legal_name = v.get("legal_name"), status = v.get("status"), country = v.get("country"), address = v.get("address"), email = v.get("email"), billing_currency = v.get("billing_currency"), phone = v.get("phone"), industry = v.get("industry")))
            return results
        else:
            print("No results.")
            return None

    def get_tag(self, id: int) -> InvgateTag:
        """
        Gets a single tag from Invgate and returns an InvgateTag object.

        Arguments:
            id* (int): The unique identifier of the tag to get from Invgate.

        Returns:
            InvgateTag: If tag is found.
            None: If tag is not found.
        """
        response = self.get_data(endpoint_path = routes.tag(id))
        if response:
            return InvgateTag(id = response.get("id"), name = response.get("name"), color = response.get("color"), description = response.get("description"), smart_tag = response.get("smart_tag"), locked = response.get("locked"))
        return None

    def get_tags(self, page: str = None) -> dict:
        """
        Gets all tags on the specified page from Invgate and returns the count, previous page, next page, and a list of InvgateTag objects. If no page is specified, returns data from the first page.
        Arguments:
            page (str): Specifies which page to get data from. If it's not specified, data will be accessed from the first page.
        
        Returns:
            dict[int, str, str, list[InvgateTag]]: If tags are found, there is a previous URL, and a next URL.
            dict[int, str, list[InvgateTag]]: If tags are found, there is a previous URL, or a new URL.
            dict[int, list[InvgateTag]]: If tags are found.
            None: If no tags are found.
        """
        if page:
            response = self.get_data(endpoint_path = routes.tags(), page = page)
        else:
            response = self.get_data(endpoint_path = routes.tags())

        if response and response["results"]:
            results = {"count": response.get("count")}

            if response["next"]:
                results["next"] = response.get("next")

            if response["previous"]:
                results["previous"] = response.get("previous")

            tags = response.get("results")
            results["tags"] = []

            for t in tags:
                results["tags"].append(InvgateTag(id = t.get("id"), name = t.get("name"), color = t.get("color"), description = t.get("description"), smart_tag = t.get("smart_tag"), locked = t.get("locked")))
            return results
        else:
            print("No results.")
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
        parameter_count = 0
        for parameter in [id, order_number]:
            if parameter:
                parameter_count += 1

        if parameter_count < 1:
            print("Get Purchase Order failed: Please provide a field to fetch the purchase order by.")
            return None
        elif parameter_count > 1:
            print("Get Purchase Order failed: Please provide only one field to fetch the purchase order by.")
            return None
        else:
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
        if id and name:
            response = self.get_data(endpoint_path = routes.manufacturer(id))
        elif id:
            response = self.get_data(endpoint_path = routes.manufacturer(id))
        elif name:
            response = self.get_data(endpoint_path = routes.manufacturers(), query = f"name={name}").get("results")[0]
        if response:
            return InvgateManufacturer(id = response.get("id"), name = response.get("name"))
        return None

    def get_manufacturers(self, page = None) -> dict:
        """
        Gets all manufacturers on the specified page from Invgate and returns the count, previous page, next page, and a list of InvgateManufacturer objects. If no page is specified, returns data from the first page.
        Arguments:
            page (str): Specifies which page to get data from. If it's not specified, data will be accessed from the first page.
        
        Returns:
            dict[int, str, str, list[InvgateManufacturer]]: If manufacturers are found, there is a previous URL, and a next URL.
            dict[int, str, list[InvgateManufacturer]]: If manufacturers are found, there is a previous URL, or a new URL.
            dict[int, list[InvgateManufacturer]]: If manufacturers are found.
            None: If no manufacturers are found.
        """
        if page:
            response = self.get_data(endpoint_path = routes.manufacturers(), page = page)
        else:
            response = self.get_data(endpoint_path = routes.manufacturers())

        if response and response["results"]:
            results = {"count": response.get("count")}

            if response["next"]:
                results["next"] = response.get("next")

            if response["previous"]:
                results["previous"] = response.get("previous")

            manufacturers = response.get("results")
            results["manufacturers"] = []

            for m in manufacturers:
                results["manufacturers"].append(InvgateManufacturer(id = m.get("id"), name = m.get("name")))
            return results
        else:
            print("No results.")
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
            return InvgateHealth(computer = response.get("computer"), updated_at = response.get("updated_at"), health_rule = response.get("health_rule"), status = response.get("status"))
        return None

    def get_healths(self, page: str = None) -> dict:
        """
        Gets all health on the specified page from Invgate and returns the count, previous page, next page, and a list of InvgateHealth objects. If no page is specified, returns data from the first page.
        Arguments:
            page (str): Specifies which page to get data from. If it's not specified, data will be accessed from the first page.
        
        Returns:
            dict[int, str, str, list[InvgateHealth]]: If healths are found, there is a previous URL, and a next URL.
            dict[int, str, list[InvgateHealth]]: If healths are found, there is a previous URL, or a new URL.
            dict[int, list[InvgateHealth]]: If healths are found.
            None: If no healths are found.
        """
        if page:
            response = self.get_data(endpoint_path = routes.healths(), page = page)
        else:
            response = self.get_data(endpoint_path = routes.healths())
        if response and response["results"]:
            results = {"count": response.get("count")}

            if response["next"]:
                results["next"] = response.get("next")

            if response["previous"]:
                results["previous"] = response.get("previous")

            healths = response.get("results")
            results["healths"] = []

            for h in healths:
                results["healths"].append(InvgateHealth(computer = h.get("computer"), updated_at = h.get("updated_at"), health_rule = h.get("health_rule"), status = h.get("status")))
            return results
        else:
            print("No results.")
            return None

    def get_status(self, id: int) -> InvgateStatus:
        """
        Gets a single status from Invgate and returns an InvgateStatus object.

        Arguments:
            id* (int): The unique identifier of the status to get from Invgate.

        Returns:
            InvgateStatus: If status is found.
            None: If status is not found.
        """
        response = self.get_data(endpoint_path = routes.status(), v1 = True, query = f"ids={id}")
        if response:
            data = response.get("data")[0]
            return InvgateStatus(id = data.get("id"), name = data.get("attributes").get("name"), description = data.get("attributes").get("description"), behavior = data.get("attributes").get("behavior"), is_default = data.get("attributes").get("is_default"))
        return None

    def get_statuses(self, page: str = None) -> dict:
        """
        Gets all statuses on the specified page from Invgate and returns the count, previous page, next page, and a list of InvgateStatus objects. If no page is specified, returns data from the first page.
        Arguments:
            page (str): Specifies which page to get data from. If it's not specified, data will be accessed from the first page.
        
        Returns:
            dict[int, str, str, list[InvgateStatus]]: If statuses are found, there is a previous URL, and a next URL.
            dict[int, str, list[InvgateStatus]]: If statuses are found, there is a previous URL, or a new URL.
            dict[int, list[InvgateStatus]]: If statuses are found.
            None: If no statuses are found.
        """
        if page:
            response = self.get_data(endpoint_path = routes.status(), page = page, v1 = True)
        else:
            response = self.get_data(endpoint_path = routes.status(), v1 = True)
        if response and response["data"]:
            links = response.get("links")
            results = {}
            if links["next"]:
                results["next"] = links.get("next")
            if links["prev"]:
                results["previous"] = links.get("prev")
            results["statuses"] = []

            data = response.get("data")
            for d in data:
                results["statuses"].append(InvgateStatus(id = d.get("id"), name = d.get("attributes").get("name"), description = d.get("attributes").get("description"), behavior = d.get("attributes").get("behavior"), is_default = d.get("attributes").get("is_default")))
            return results
        else:
            print("No results.")
            return None

    def get_location(self, id: int) -> InvgateLocation:
        """
        Gets a single location from Invgate and returns an InvgateLocation object.

        Arguments:
            id* (int): The unique identifier of the location to get from Invgate.

        Returns:
            InvgateLocation: If location is found.
            None: If location is not found.
        """
        response = self.get_data(endpoint_path = routes.location(id), v1 = True)
        if response and response["data"]:
            data = response.get("data")
            return InvgateLocation(id = data.get("id"), name = data.get("attributes").get("name"), full_path = data.get("attributes").get("full_path"), description = data.get("attributes").get("description"))
        return None

    def get_locations(self, page: str = None) -> dict:
        """
        Gets all locations on the specified page from Invgate and returns the count, previous page, next page, and a list of InvgateLocation objects. If no page is specified, returns data from the first page.
        Arguments:
            page (str): Specifies which page to get data from. If it's not specified, data will be accessed from the first page.
        
        Returns:
            dict[int, str, str, list[InvgateLocation]]: If locations are found, there is a previous URL, and a next URL.
            dict[int, str, list[InvgateLocation]]: If locations are found, there is a previous URL, or a new URL.
            dict[int, list[InvgateLocation]]: If locations are found.
            None: If no locations are found.
        """
        if page:
            response = self.get_data(endpoint_path = routes.locations(), page = page, v1 = True)
        else:
            response = self.get_data(endpoint_path = routes.locations(), v1 = True)

        if response and response["data"]:
            links = response.get("links")
            results = {}
            if links["next"]:
                results["next"] = links.get("next")

            if links["prev"]:
                results["previous"] = links.get("prev")
            results["locations"] = []

            data = response.get("data")

            for d in data:
                results["locations"].append(InvgateLocation(id = d.get("id"), name = d.get("attributes").get("name"), full_path = d.get("attributes").get("full_path"), description = d.get("attributes").get("description")))
        else:
            print("No results")
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
            if response["version"]["program"]["manufacturer"]:
                manufacturer = InvgateManufacturer(id = response.get("version").get("program").get("manufacturer").get("id"), name = response.get("version").get("program").get("manufacturer").get("name"))
            else:
                manufacturer = None

            return InvgateSoftware(id = response.get("id"), resource_type = response.get("resource_type"), install_date = response.get("install_date"), install_path = response.get("install_path"), uninstall_call = response.get("uninstall_call"), computer = response.get("computer"), version = response.get("version").get("version"), internal_version = response.get("version").get("internal_version"), edition = response.get("version").get("edition"), name = response.get("version").get("program").get("name"), manufacturer = manufacturer, license = response.get("version").get("program").get("license"), category = response.get("version").get("program").get("category"), types = response.get("version").get("program").get("types"), types_key = response.get("version").get("program").get("types_key"), tags = response.get("version").get("program").get("tags"), is_metering_enabled = response.get("version").get("program").get("is_metering_enabled"))
        else:
            return None

    def get_softwares(self, page: str = None) -> dict:
        """
        Gets all software on the specified page from Invgate and returns the count, previous page, next page, and a list of InvgateSoftware objects. If no page is specified, returns data from the first page.
        Arguments:
            page (str): Specifies which page to get data from. If it's not specified, data will be accessed from the first page.
        
        Returns:
            dict[int, str, str, list[InvgateSoftware]]: If softwares are found, there is a previous URL, and a next URL.
            dict[int, str, list[InvgateSoftware]]: If softwares are found, there is a previous URL, or a new URL.
            dict[int, list[InvgateSoftware]]: If softwares are found.
            None: If no softwares are found.
        """
        if page:
            response = self.get_data(endpoint_path = routes.softwares(), page = page)
        else:
            response = self.get_data(endpoint_path = routes.softwares())

        if response and response["results"]:
            results = {"count": response.get("count")}

            if response["next"]:
                results["next"] = response.get("next")

            if response["previous"]:
                results["previous"] = response.get["previous"]

            softwares = response.get("results")
            results["softwares"] = []

            for s in softwares:
                if s["version"]["program"]["manufacturer"]:
                    manufacturer = InvgateManufacturer(id = s.get("version").get("program").get("manufacturer").get("id"), name = s.get("version").get("program").get("manufacturer").get("name"))
                else:
                    manufacturer = None
                results["softwares"].append(InvgateSoftware(id = s.get("id"), resource_type = s.get("resource_type"), install_date = s.get("install_date"), install_path = s.get("install_path"), uninstall_call = s.get("uninstall_call"), computer = s.get("computer"), version = s.get("version").get("version"), internal_version = s.get("version").get("internal_version"), edition = s.get("version").get("edition"), name = s.get("version").get("program").get("name"), manufacturer = manufacturer, license = s.get("version").get("program").get("license"), category = s.get("version").get("program").get("category"), types = s.get("version").get("program").get("types"), types_key = s.get("version").get("program").get("types_key"), tags = s.get("version").get("program").get("tags"), is_metering_enabled = s.get("version").get("program").get("is_metering_enabled")))
            return results
        else:
            print("No results.")
            return None

    def get_asset(self, id: int = None, name: str = None) -> InvgateAsset:
        """
        Gets a single asset from Invgate and returns an InvgateAsset object.
        
        Arguments:
            id (int): The unique identifier of the asset to get from Invgate.
            name (str): The name of the asset to get from Invgate.

        Returns:
            InvgateAsset: If asset is found.
            None: If asset is not found.
        """
        if id and name:
            response = self.get_data(endpoint_path = routes.asset(id))
        elif id:
            response = self.get_data(endpoint_path = routes.asset(id))
        elif name:
            response = self.get_data(endpoint_path = routes.assets(), query = f"name={name}").get("results")[0]


        if response:
            if response["status"]:
                status = self.get_status(response.get("status"))
            else:
                status = None

            if response["location"]:
                location = self.get_location(response.get("location"))
            else:
                location = None

            if response["owner"]:
                owner = self.get_user(response.get("owner"))
            else:
                owner = None

            if response["finance"]:
                finance = self.get_finance(response.get("finance"))
            else:
                finance = None

            if response["manufacturer"]:
                manufacturer = self.get_manufacturer(name = response.get("manufacturer"))
            else:
                manufacturer = None

            return InvgateAsset(name = response.get("name"), id = response.get("id"), serial = response.get("serial"), inventory_id = response.get("inventory_id"), asset_physical_tag = response.get("asset_physical_tag"), created_at = response.get("created_at"), reported_at = response.get("reported_at"), updated_at = response.get("updated_at"), status = status, location = location, owner = owner, finance = finance, manufacturer = manufacturer, model = response.get("model"), commercial_model = response.get("commercial_model"), asset_type = response.get("asset_type"), default_ip = response.get("default_ip"), mac_address = response.get("mac_address"), asset_type_code = response.get("asset_type_code"), format = response.get("format"))
        else:
            return None

    def get_assets(self, page: str = None) -> dict:
        """
        Gets all assets on the specified page from Invgate and returns the count, previous page, next page, and a list of InvgateAsset objects. If no page is specified, returns data from the first page.
        
        Arguments:
            page (str): Specifies which page to get data from. If it's not specified, data will be accessed from the first page.

        Returns:
            dict[int, str, str, list[InvgateAsset]]: if assets found, there is a previous URL, and a next URL.
            dict[int, str, list[InvgateAsset]]: If assets are found, there is a previous URL, or a next URL
            dict[int, list[InvgateAsset]]: If assets are found.
            None: If no assets are found.
        """
        if page:
            response = self.get_data(endpoint_path = routes.assets(), page = page)
        else:
            response = self.get_data(endpoint_path = routes.assets())

        if response and response["results"]:
            results = {"count": response.get("count")}

            if response["next"]:
                results["next"] = response.get("next")

            if response["previous"]:
                results["previous"] = response.get("previous")

            assets = response.get("results")
            results["assets"] = []
    
            for a in assets:
                if a["status"]:
                    status = self.get_status(a.get("status"))
                else:
                    status = None

                if a["location"]:
                    location = self.get_location(a.get("location"))
                else:
                    location = None

                if a["owner"]:
                    owner = self.get_user(a.get("owner"))
                else:
                    owner = None

                if a["finance"]:
                    finance = self.get_finance(a.get("finance"))
                else:
                    finance = None

                if a["manufacturer"]:
                    manufacturer = self.get_manufacturer(name = a.get("manufacturer"))
                else:
                    manufacturer = None

                results["assets"].append(InvgateAsset(name = a.get("name"), serial = a.get("serial"), inventory_id = a.get("inventory_id"), asset_physical_tag = a.get("asset_physical_tag"), created_at = a.get("created_at"), reported_at = a.get("reported_at"), updated_at = a.get("updated_at"), status = status, location = location, owner = owner, finance = finance, manufacturer = manufacturer, model = a.get("model"), commercial_model = a.get("commercial_model"), asset_type = a.get("asset_type"), default_ip = a.get("default_ip"), mac_address = a.get("mac_address"), asset_type_code = a.get("asset_type_code"), format = a.get("format")))
            return results
        else:
            return None

    def get_operating_system_update(self, id: int) -> InvgateOperatingSystemUpdate:
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
            return InvgateOperatingSystemUpdate(id = response.get("id"), install_date = response.get("install_date"), status = response.get("status"), computer = response.get("computer"), version = response.get("os_update_version").get("version"), release_date = response.get("os_update_version").get("release_date"), short_name = response.get("os_update_version").get("os_update").get("short_name"), name = response.get("os_update_version").get("os_update").get("name"), update_type = response.get("os_update_version").get("os_update").get("update_type"), os_type = response.get("os_update_version").get("os_update").get("os_type"), severity = response.get("os_update_version").get("os_update").get("severity"), support_url = response.get("os_update_version").get("os_update").get("support_url"))
        else:
            return None

    def get_operating_system_updates(self, page: str = None) -> dict:
        """
        Gets all operating system updates on the specified page from Invgate and returns the count, previous page, next page, and a list of InvgateOperatingSystemUpdate objects. If no page is specified, returns data from the first page.
        Arguments:
            page (str): Specifies which page to get data from. If it's not specified, data will be accessed from the first page.
        
        Returns:
            dict[int, str, str, list[InvgateOperatingSystemUpdate]]: If operating system updates are found, there is a previous URL, and a next URL.
            dict[int, str, list[InvgateOperatingSystemUpdate]]: If operating system updates are found, there is a previous URL, or a new URL.
            dict[int, list[InvgateOperatingSystemUpdate]]: If operating system updates are found.
            None: If no operating system updates are found.
        """
        if page:
            response = self.get_data(endpoint_path = routes.operating_system_updates(), page = page)
        else:
            response = self.get_data(endpoint_path = routes.operating_system_updates())

        if response and response["results"]:
            results = {"count": response.get("count")}

            if response["next"]:
                results["next"] = response.get("next")

            if response["previous"]:
                results["previous"] = response.get("previous")

            operating_system_updates = response.get("results")
            results["operating_system_updates"] = []

            for os_update in operating_system_updates:
                results["operating_system_updates"].append(InvgateOperatingSystemUpdate(id = os_update.get("id"), install_date = os_update.get("install_date"), status = os_update.get("status"), computer = os_update.get("computer"), version = os_update.get("os_update_version").get("version"), release_date = os_update.get("os_update_version").get("release_date"), short_name = os_update.get("os_update_version").get("os_update").get("short_name"), name = os_update.get("os_update_version").get("os_update").get("name"), update_type = os_update.get("os_update_version").get("os_update").get("update_type"), os_type = os_update.get("os_update_version").get("os_update").get("os_type"), severity = os_update.get("os_update_version").get("os_update").get("severity"), support_url = os_update.get("os_update_version").get("os_update").get("support_url")))
            return results
        else:
            print("No results.")
            return None

    def get_operating_system_updates_for_computer(self, computer_id: int) -> dict:
        """
        Gets all operating system updates that belong to the specified asset id and returns them as InvgateOperatingSystemUpdate objects
        Arguments:
            computer_id* (int): The unique identifier of the asset that the operating system updates belong to. 
        Returns:
            dict[int, list[InvgateOperatingSystemUpdate]]: If operating system updates are found.
            None: If no operating system updates are found.
        """
        response = self.get_data(endpoint_path = routes.operating_system_updates(), query = f"asset_id={computer_id}")
        if response and response["results"]:
            results = {"count": response.get("count")}
            results["operating_system_updates"] = []

            while True:
                operating_system_updates = response.get("results")
                for os_update in operating_system_updates:
                    results["operating_system_updates"].append(InvgateOperatingSystemUpdate(id = os_update.get("id"), install_date = os_update.get("install_date"), status = os_update.get("status"), computer = os_update.get("computer"), version = os_update.get("os_update_version").get("version"), release_date = os_update.get("os_update_version").get("release_date"), short_name = os_update.get("os_update_version").get("os_update").get("short_name"), name = os_update.get("os_update_version").get("os_update").get("name"), update_type = os_update.get("os_update_version").get("os_update").get("update_type"), os_type = os_update.get("os_update_version").get("os_update").get("os_type"), severity = os_update.get("os_update_version").get("os_update").get("severity"), support_url = os_update.get("os_update_version").get("os_update").get("support_url")))
                if response["next"]:
                    response = self.get_data(full_path = response.get("next"))
                else:
                    break
            return results

    def get_software_for_computer(self, computer_id: int) -> list:
        """
        Gets software installations that belong to the specified asset id and returns them as InvgateSoftware objects
        Arguments:
            computer_id* (int): The unique identifier of the asset that the software installations belong to. 
        Returns:
            dict[int, list[InvgateSoftware]]: If software installations are found.
            None: If no software installations are found.
        """
        response = self.get_data(endpoint_path = routes.softwares(), query = f"asset_id={computer_id}")
        if response and response["results"]:
            results = {"count": response.get("count")}
            results["softwares"] =  []
            while True:
                softwares = response.get("results")
                for s in softwares:
                    if s["version"]["program"]["manufacturer"]:
                        manufacturer = InvgateManufacturer(id = s.get("version").get("program").get("manufacturer").get("id"), name = s.get("version").get("program").get("manufacturer").get("name"))
                    else:
                        manufacturer = None

                    results["softwares"].append(InvgateSoftware(id = s.get("id"), resource_type = s.get("resource_type"), install_date = s.get("install_date"), uninstall_call = s.get("uninstall_call"), computer = s.get("computer"), version = s.get("version").get("version"), internal_version = s.get("version").get("internal_version"), edition = s.get("version").get("edition"), name = s.get("version").get("program").get("name"), manufacturer = manufacturer, license = s.get("version").get("program").get("license"), category = s.get("version").get("program").get("cateogry"), types = s.get("version").get("program").get("types"), types_key = s.get("version").get("program").get("types_key"), tags = s.get("version").get("program").get("tags"), is_metering_enabled = s.get("version").get("program").get("is_metering_enabled")))

                if response["next"]:
                    response = self.get_data(full_path = response.get("next"))
                else:
                    break
            return results
        else:
            print("No results.")
            return None

    def get_purchase_order_by_order_id(self, order_id: str) -> InvgatePurchaseOrder:
        """
        Gets a purchase order from Invgate by filtering by the purchase order's name.
        Arguments:
            order_id: The purchase order's name.
        
        Returns:
            InvgatePurchaseOrder: If purchase order is found.
            None: If purchase order is not found.
        """
        response = self.get_data(endpoint_path = routes.purchase_orders())
        po = None

        while True:
            purchase_orders = response.get("results")
            for purchase_order in purchase_orders:
                if order_id == purchase_order.get("order_number"):
                    po = purchase_order
                    break
            if po:
                break
            if response["next"]:
                response = self.get_data(full_path = response.get("next"))

        if po:
            return InvgatePurchaseOrder(id = po.get("id"), order_number = po.get("order_number"), vendor = po.get("vendor"), purchase_order_type = po.get("purchase_order_type"), creation_date = po.get("creation_date"), expected_delivery_date = po.get("expected_delivery_date"), date_delivered = po.get("date_delivered"), ship_method = po.get("ship_method"), ship_to = po.get("ship_to"), shipping_address = po.get("shipping_address"), ship_instructions = po.get("ship_instructions"), billing_address = po.get("billing_address"), status = po.get("status"), subtotal = po.get("subtotal"), freight = po.get("freight"), handling = po.get("handling"), tax = po.get("tax"), total_cost = po.get("total_cost"), cost_center = po.get("cost_center"), contract = po.get("contract"), requested_by = po.get("requested_by"))
        else:
            return None

    def get_asset_with_collections(self, id: int = None, name: str = None) -> InvgateAsset:
        """
        Gets a single asset from Invgate along with its collections and returns an InvgateAsset object.
        
        Arguments:
            id (int): The unique identifier of the asset to get from Invgate.
            name (str): The name of the asset to get from Invgate.

        Returns:
            InvgateAsset: If asset is found.
            None: If asset is not found.
        """
        if id and name:
            response = self.get_data(endpoint_path = routes.asset(id))
        elif id:
            response = self.get_data(endpoint_path = routes.asset(id))
        elif name:
            response = self.get_data(endpoint_path = routes.assets(), query = f"name={name}").get("results")[0]

        if response:
            if response["status"]:
                status = self.get_status(response.get("status"))
            else:
                status = None

            if response["location"]:
                location = self.get_location(response.get("location"))
            else:
                location = None

            if response["owner"]:
                owner = self.get_user(response.get("owner"))
            else:
                owner = None

            if response["finance"]:
                finance = self.get_finance(response.get("finance"))
            else:
                finance = None

            if response["manufacturer"]:
                manufacturer = self.get_manufacturer(name = response.get("manufacturer"))
            else:
                manufacturer = None

            asset = InvgateAsset(name = response.get("name"), id = response.get("id"), serial = response.get("serial"), inventory_id = response.get("inventory_id"), asset_physical_tag = response.get("asset_physical_tag"), created_at = response.get("created_at"), reported_at = response.get("reported_at"), updated_at = response.get("updated_at"), status = status, location = location, owner = owner, finance = finance, manufacturer = manufacturer, model = response.get("model"), commercial_model = response.get("commercial_model"), asset_type = response.get("asset_type"), default_ip = response.get("default_ip"), mac_address = response.get("mac_address"), asset_type_code = response.get("asset_type_code"), format = response.get("format"))
            health = self.get_health(asset.id)
            software = self.get_software_for_computer(asset.id)
            operating_system_updates = self.get_operating_system_updates_for_computer(asset.id)

            if software and operating_system_updates:
                asset.populate_collections(health = health, software = software.get("softwares"), operating_system_updates = operating_system_updates.get("operating_system_updates"))
            elif software:
                asset.populate_collections(health = health, software = software.get("softwares"))
            elif operating_system_updates:
                asset.populate_collections(health = health, operating_system_updates = operating_system_updates.get("operating_system_updates"))
            return asset
        else:
            return None

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

                

                
    def load_data(self) -> dict:

        results = {}

        # Vendors
        temp_vendors = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.vendors()))
        for vendor in response.get("data"):
            temp_vendors[vendor.get("id")] = InvgateVendor(id = vendor.get("id"), company_name = vendor.get("company_name"), legal_name = vendor.get("legal_name"), status = vendor.get("status"), country = vendor.get("country"), address = vendor.get("address"), email = vendor.get("email"), billing_currency = vendor.get("billing_currency"), phone = vendor.get("phone"), industry = vendor.get("industry"))

        # Manufacturers
        temp_manufacturers = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.manufacturers()))
        for manufacturer in response.get("data"):
            temp_manufacturers[manufacturer.get("name")] = InvgateManufacturer(name = manufacturer.get("name"), id = manufacturer.get("id"))

        # Locations
        temp_locations = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.locations(), v1 = True))
        for location in response.get("data"):
            temp_locations[location.get("id")] = InvgateLocation(name = location.get("attributes").get("name"), id = location.get("id"), full_path = location.get("attributes").get("full_path"), description = location.get("attributes").get("description"))

        # Statuses
        temp_statuses = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.status(), v1 = True))
        for status in response.get("data"):
            temp_statuses[status.get("id")] = InvgateStatus(id = status.get("id"), name = status.get("attributes").get("name"), description = status.get("attributes").get("description"), behavior = status.get("attributes").get("behavior"), is_default = status.get("attributes").get("is_default"))

        # Purchase Orders
        temp_purchase_orders = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.purchase_orders()))
        for po in response.get("data"):
            if po.get("vendor"):
                vendor = temp_vendors.get(po.get("vendor"))
            else:
                vendor: None
            temp_purchase_orders[po.get("order_number")] = InvgatePurchaseOrder(order_number = po.get("order_number"), id = po.get("id"), vendor = vendor, purchase_order_type = po.get("purchase_order_type"), creation_date = po.get("creation_date"), expected_delivery_date = po.get("expected_delivery_date"), date_delivered = po.get("date_delivered"), ship_method = po.get("ship_method"), ship_to = po.get("ship_to"), shipping_address = po.get("shipping_address"), ship_instructions = po.get("ship_instructions"), billing_address = po.get("billing_address"), status = po.get("status"), subtotal = po.get("subtotal"), freight = po.get("freight"), handling = po.get("handling"), tax = po.get("tax"), total_cost = po.get("total_cost"), cost_center = po.get("cost_center"), contract = po.get("contract"), requested_by = po.get("requested_by"), items = po.get("items"))

        # Finance
        temp_finance = {}
        response = self.get_all_pages(self.get_data(endpoint_path = routes.financials()))
        for finance in response.get("data"):
            if finance.get("vendor"):
                vendor = temp_vendors.get(finance.get("vendor"))
            else:
                vendor = None

            if finance.get("purchase_order"):
                purchase_order = temp_purchase_orders.get(finance.get("order_id"))
            else:
                purchase_order = None

            temp_finance[finance.get("id")] = InvgateFinance(asset = finance.get("asset"), id = finance.get("id"), acquisition_type = finance.get("acquisition_type"), acquisition_date = finance.get("acquisition_date"), acquisition_price = finance.get("acquisition_price"), actual_price = finance.get("actual_price"), residual_value = finance.get("residual_value"), depreciation_percentage = finance.get("depreciation_percentage"), warranty_date = finance.get("warranty_date"), vendor = vendor, cost_center = finance.get("cost_center"), purchase_order = purchase_order, invoice_id = finance.get("invoice_id"))

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

            if user.get("location"):
                location = temp_locations.get(user.get("location").get("id"))
            else:
                location = None
            user_object = InvgateUser(name = user.get("name"), email = user.get("email"), id = user.get("id"), date_of_birth = user.get("date_of_birth"), employee_id = user.get("employee_id"), position = user.get("position"), department = user.get("department"), company = user.get("company"), phone = user.get("phone"), cellphone = user.get("cellphone"), address = user.get("address"), person_type = user.get("person_type"), user = user.get("user"), manager_id = manager_id, manager_name = manager_name, manager_email = manager_email, location = location, cost_center = user.get("cost_center"))
            temp_users[user_object.id] = user_object
            results["users"].append(user_object)

        # Assets
        results["assets"] = []
        response = self.get_all_pages(self.get_data(endpoint_path = routes.assets()))
        for asset in response.get("data"):
            if asset.get("status"):
                status = temp_statuses.get(asset.get("status"))
            else:
                status = None

            if asset.get("location"):
                location = temp_locations.get(asset.get("location"))
            else:
                location = None

            if asset.get("owner"):
                owner = temp_users.get(asset.get("owner"))
            else:
                owner = None

            if asset.get("finance"):
                finance = temp_finance.get(asset.get("finance"))
            else:
                finance = None

            if asset.get("manufacturer"):
                manufacturer = temp_manufacturers.get(asset.get("manufacturer"))
            else:
                manufacturer = None

            results["assets"].append(InvgateAsset(name = asset.get("name"), id = asset.get("id"), serial = asset.get("serial"), inventory_id = asset.get("inventory_id"), asset_physical_tag = asset.get("asset_physical_tag"), created_at = asset.get("created_at"), reported_at = asset.get("reported_at"), updated_at = asset.get("updated_at"), status = status, location = location, owner = owner, finance = finance, manufacturer = manufacturer, model = asset.get("model"), commercial_model = asset.get("commercial_model"), asset_type = asset.get("asset_type"), default_ip = asset.get("default_ip"), mac_address = asset.get("mac_address"), asset_type_code = asset.get("asset_type_code"), format = asset.get("format")))

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