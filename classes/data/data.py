import copy

from classes.invgate.invgate_connection import InvgateConnection
from classes.invgate.invgate_asset import InvgateAsset
from classes.invgate.invgate_user import InvgateUser
from classes.data.fields import Fields, Field
from classes.data.collections import Collections
from classes.data.conditions import Condition            

class FilterParameter:
    def __init__(self, filter_value, field: Field, condition: Condition, operator: str = None):
        if type(filter_value) == str:
            self.filter_value = filter_value.lower()
        else:
            self.filter_value = filter_value

        self.field: Field = None

        if field.filterable:
            self.field = field
        self.condition: Condition = condition
        self.operator: str = None
        if operator:
            self.operator = operator
        else:
            self.operator = "initial"

    def match_asset_field(self, asset: InvgateAsset):
        match self.field:
            case Fields.serial:
                value = asset.serial.lower() if asset.serial else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.created_at:
                value = asset.created_at if asset.created_at else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.reported_at:
                value = asset.reported_at if asset.reported_at else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.updated_at:
                value = asset.updated_at if asset.updated_at else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.status:
                value = asset.status.name.lower() if asset.status and asset.status.name else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.owner_email:
                value = asset.owner.email.lower() if asset.owner and asset.owner.email else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.asset_location:
                value = asset.location.name.lower() if asset.location and asset.location.name else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.acquisition_price:
                value = asset.finance.acquisition_price if asset.finance and asset.finance.acquisition_price else 0
                return self.condition.apply(value, self.filter_value)
            case Fields.acquisition_date:
                value = asset.finance.acquisition_date if asset.finance and asset.finance.acquisition_date else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.vendor:
                value = asset.finance.vendor.company_name.lower() if asset.finance and asset.finance.vendor and asset.finance.vendor.company_name else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.residual_value:
                value = asset.finance.residual_value if asset.finance and asset.finance.residual_value else 0
                return self.condition.apply(value, self.filter_value)
            case Fields.actual_price:
                value = asset.finance.actual_price if asset.finance and asset.finance.actual_price else 0
                return self.condition.apply(value, self.filter_value)
            case Fields.purchase_order:
                value = asset.finance.purchase_order.order_number if asset.finance and asset.finance.purchase_order and asset.finance.purchase_order.order_number else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.invoice:
                value = asset.finance.invoice_id.lower() if asset.finance and asset.finance.invoice_id else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.manufacturer:
                value = asset.manufacturer.name.lower() if asset.manufacturer and asset.manufacturer.name else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.model:
                value = asset.model.lower() if asset.model else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.commercial_model:
                value = asset.commercial_model.lower() if asset.commercial_model else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.asset_type:
                value = asset.asset_type.lower() if asset.asset_type else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.default_ip:
                value = asset.default_ip if asset.default_ip else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.mac_address:
                value = asset.mac_address.lower() if asset.mac_address else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.format:
                value = asset.format.lower() if asset.format else ""
                return self.condition.apply(value, self.filter_value)
        return False

    def match_user_field(self, user: InvgateUser):
        match self.field:
            case Fields.employee_id:
                value = user.employee_id.lower() if user.employee_id else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.position:
                value = user.position.lower() if user.position else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.department:
                value = user.department.lower() if user.department else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.manager_name: 
                value = user.manager_name.lower() if user.manager_name else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.manager_email:
                value = user.manager_email.lower() if user.manager_email else ""
                return self.condition.apply(value, self.filter_value)
            case Fields.user_location:
                value = user.location.name.lower() if user.location and user.location.name else ""
                return self.condition.apply(value, self.filter_value)
        return False

class FilterParameters:
    def __init__(self, parameters: list[FilterParameter]):
        self.user_parameters: list[FilterParameter] = []
        self.asset_parameters: list[FilterParameter] = []

        for parameter in parameters.copy():
            if parameter:
                if parameter.operator == "initial":
                    if parameter.field.contained_within(Collections.users):
                        self.user_parameters.append(parameter)
                        parameters.remove(parameter)
                    if parameter.field.contained_within(Collections.assets):
                        self.asset_parameters.append(parameter)
                        parameters.remove(parameter)


        for parameter in parameters:
            if parameter:
                if parameter.field.contained_within(Collections.users):
                    self.user_parameters.append(parameter)
                if parameter.field.contained_within(Collections.assets):
                    self.asset_parameters.append(parameter)

    def filter_record(self, user: InvgateUser = None, asset: InvgateAsset = None) -> bool:
        matched: bool = True
        if user:
            for parameter in self.user_parameters:
                if parameter.operator == "and":
                    matched = matched and parameter.match_user_field(user)
                elif parameter.operator == "or":
                    matched = matched or parameter.match_user_field(user)
                else:
                    matched = parameter.match_user_field(user)
        elif asset:
            for parameter in self.asset_parameters:
                if parameter.operator == "and":
                    matched = matched and parameter.match_asset_field(asset)
                elif parameter.operator == "or":
                    matched = matched or parameter.match_asset_field(asset)
                else:
                    matched = parameter.match_asset_field(asset)

        return matched
    def get_all_parameters(self) -> list[FilterParameter]:
        return self.user_parameters + self.asset_parameters

    def add_parameters(self, parameters: list[FilterParameter]) -> None:
        for parameter in parameters:
            if parameter.field.filterable:
                if parameter.operator == "initial":
                    parameter.operator = "and"

                if parameter.field.contained_within(Collections.assets):
                    self.asset_parameters.append(parameter)
                elif parameter.field.contained_within(Collections.users):
                   self.user_parameters.append(parameter) 

class SearchParameter:
    def __init__(self, search_phrase: str, field_to_search: Field):
        self.tags: list[str] = search_phrase.split()
        self.field: Field = None
        if field_to_search.searchable:
            self.field = field_to_search

    def match_asset_field(self, asset: InvgateAsset) -> bool:
        asset_name = asset.name.lower() if asset.name else ""
        owner_name = asset.owner.name.lower() if asset.owner and asset.owner.name else ""
        model = asset.model.lower() if asset.model else ""
        commercial_model = asset.commercial_model.lower() if asset.commercial_model else ""

        match self.field:
            case Fields.asset_name:
                return all(tag.lower() in asset_name for tag in self.tags)
            case Fields.owner_name:
                return all(tag.lower() in owner_name for tag in self.tags)
            case Fields.model:
                return all(tag.lower() in model for tag in self.tags)
            case Fields.commercial_model:
                return all(tag.lower() in commercial_model for tag in self.tags)
            case _:
                return False
    def match_user_field(self, user: InvgateUser) -> bool:
        user_name = user.name.lower() if user.name else ""
        email = user.email.lower() if user.email else ""
        employee_id = user.employee_id.lower() if user.employee_id else ""

        match self.field:
            case Fields.user_name:
                return all(tag.lower() in user_name for tag in self.tags)
            case Fields.email:
                return all(tag.lower() in email for tag in self.tags)
            case Fields.employee_id:
                return all(tag.lower() in employee_id for tag in self.tags)
            case _:
                return False

class SearchParameters:
    def __init__(self, parameters: list[SearchParameter]):
        self.asset_parameters: list[SearchParameter] = []
        self.user_parameters: list[SearchParameter] = []

        for parameter in parameters:
            if parameter:
                if parameter.field.contained_within(Collections.assets):
                    self.asset_parameters.append(parameter)
                if parameter.field.contained_within(Collections.users):
                    self.user_parameters.append(parameter)
        
    def search_record(self, asset: InvgateAsset = None, user: InvgateUser = None) -> bool:
        if asset:
            for parameter in self.asset_parameters:
                if parameter.match_asset_field(asset):
                    return True

        elif user:
            for parameter in self.user_parameters:
                if parameter.match_user_field(user):
                    return True
        return False

    def get_all_parameters(self) -> list[SearchParameter]:
        return self.user_parameters + self.asset_parameters

    def add_parameters(self, parameters: list[SearchParameter]) -> None:
        for parameter in parameters:
            if parameter.field.searchable:
                if parameter.field.contained_within(Collections.assets):
                    self.asset_parameters.append(parameter)
                elif parameter.field.contained_within(Collections.users):
                    self.user_parameters.append(parameter)

class OrderParameter:
    def __init__(self, field: Field, direction: str):
        self.field: Field = None

        if field.orderable:
            self.field = field

        self.reversed: bool = False
        direction = direction.lower()
        if direction == "ascending" or direction == "asc" or direction == "a":
            self.reversed = False
        elif direction == "descending" or direction == "desc" or direction == "d":
            self.reversed = True

    def sort_assets_by_field(self, assets: list[InvgateAsset]):
        if self.field:
            match self.field:
                case Fields.asset_name:
                    assets.sort(key = lambda asset: asset.name or "", reverse = self.reversed)
                    return assets
                case Fields.owner_name:
                    assets.sort(key = lambda asset: asset.owner.name if asset.owner and asset.owner.name else "", reverse = self.reversed)
                    return assets
                case Fields.serial:
                    assets.sort(key = lambda asset: asset.serial or "", reverse = self.reversed)
                    return assets
                case Fields.created_at:
                    assets.sort(key = lambda asset: asset.created_at or "", reverse = self.reversed)
                    return assets
                case Fields.reported_at:
                    assets.sort(key = lambda asset: asset.reported_at or "", reverse = self.reversed)
                    return assets
                case Fields.updated_at:
                    assets.sort(key = lambda asset: asset.updated_at or "", reverse = self.reversed)
                    return assets
                case Fields.acquisition_price:
                    assets.sort(key = lambda asset: asset.finance.acquisition_price if asset.finance and asset.finance.acquisition_price else 0, reverse = self.reversed)
                    return assets
                case Fields.acquisition_date:
                    assets.sort(key = lambda asset: asset.finance.acquisition_date if asset.finance and asset.finance.acquisition_date else "", reverse = self.reversed)
                    return assets
                case Fields.actual_price:
                    assets.sort(key = lambda asset: asset.finance.actual_price if asset.finance and asset.finance.actual_price else 0, reverse = self.reversed)
                    return assets
                case Fields.mac_address:
                    assets.sort(key = lambda asset: asset.mac_address or "", reverse = self.reversed)
                    return assets
        return assets

    def sort_users_by_field(self, users: list[InvgateUser]):
        if self.field:
            match self.field:
                case Fields.user_name:
                    users.sort(key = lambda user: user.name or "", reverse = self.reversed)
                    return users
                case Fields.email:
                    users.sort(key = lambda user: user.email or "", reverse = self.reversed)
                    return users
                case Fields.employee_id:
                    users.sort(key = lambda user: user.employee_id or "", reverse = self.reversed)
                    return users

        return users

class OrderParameters:
    def __init__(self, parameters: list[OrderParameter]):
        self.asset_parameters: list[OrderParameter] = []
        self.user_parameters: list[OrderParameter] = []

        for parameter in parameters:
            if parameter:
                if parameter.field.contained_within(Collections.assets):
                    self.asset_parameters.append(parameter)
                elif parameter.field.contained_within(Collections.users):
                    self.user_parameters.append(parameter)

    def sort_collections(self, assets: list[InvgateAsset], users: list[InvgateUser]):
        results = {}
        results["users"] = []
        results["assets"] = []
        if self.asset_parameters:
            for parameter in reversed(self.asset_parameters):
                results["assets"] = parameter.sort_assets_by_field(assets)
        else:
            results["assets"] = assets

        if self.user_parameters:
            for parameter in reversed(self.user_parameters):
                results["users"] = parameter.sort_users_by_field(users)
        else:
            results["users"] = users
        return results

    def get_all_parameters(self) -> list[OrderParameter]:
        return self.user_parameters + self.asset_parameters

    def add_parameters(self, parameters: list[OrderParameter]) -> None:
        for parameter in parameters:
            if parameter.field.orderable:
                if parameter.field.contained_within(Collections.assets):
                    self.asset_parameters.append(parameter)
                elif parameter.field.contained_within(Collections.users):
                    self.user_parameters.append(parameter)

class QueryParameters:
    def __init__(self, search_parameters: SearchParameters = None, filter_parameters: FilterParameters = None, order_parameters: OrderParameters = None):
        self.search_parameters: SearchParameters = search_parameters or SearchParameters(parameters = [])
        self.filter_parameters: FilterParameters = filter_parameters or FilterParameters(parameters = [])
        self.order_parameters: OrderParameters = order_parameters or OrderParameters(parameters = [])

    def add_search_parameters(self, search_parameters: list[SearchParameter]) -> None:
        self.search_parameters.add_parameters(search_parameters)

    def add_filter_parameters(self, filter_parameters: list[FilterParameter]) -> None:
        self.filter_parameters.add_parameters(filter_parameters)

    def add_order_parameters(self, order_parameters: list[OrderParameter]) -> None:
        self.order_parameters.add_parameters(order_parameters)

class ResultSet:
    def __init__(self, users: list[InvgateUser], assets: list[InvgateAsset], query: QueryParameters = QueryParameters()):
        self.users: list[InvgateUser] = users
        self.assets: list[InvgateAsset] = assets
        self.query: QueryParameters = query

    def filter(self, parameters: FilterParameters) -> ResultSet:   
        new_query: QueryParameters = copy.deepcopy(self.query)
        new_query.add_filter_parameters(parameters.get_all_parameters())     
        results: ResultSet = ResultSet(users = [], assets = [], query = new_query)

        for asset in self.assets:
            if parameters.filter_record(asset = asset):
                results.assets.append(asset)
        for user in self.users:
            if parameters.filter_record(user = user):
                results.users.append(user)

        return results

    def search(self, parameters: SearchParameters) -> ResultSet:
        new_query: QueryParameters = copy.deepcopy(self.query)
        new_query.add_search_parameters(parameters.get_all_parameters())
        results: ResultSet = ResultSet(users = [], assets = [], query = new_query)

        for asset in self.assets:
            if parameters.search_record(asset):
                results.assets.append(asset)

        for user in self.users:
            if parameters.search_record(user):
                results.users.append(user)

        return results

    def order(self, parameters: OrderParameters) -> ResultSet:
        new_query: QueryParameters = copy.deepcopy(self.query)
        new_query.add_order_parameters(parameters.get_all_parameters())
        sorted_data: dict = parameters.sort_collections(self.assets.copy(), self.users.copy())
        return ResultSet(users = sorted_data.get("users"), assets = sorted_data.get("assets"), query = new_query)
        
class Data:
    def __init__(self, connection: InvgateConnection):
        response = connection.load_data()

        self.assets: list[InvgateAsset] = response.get("assets")
        self.users: list[InvgateUser] = response.get("users")

    def query_data(self, query_parameters: QueryParameters) -> ResultSet:
        results: ResultSet = ResultSet(self.users, self.assets)      
        if query_parameters.filter_parameters:
            results = results.filter(query_parameters.filter_parameters)

        if query_parameters.search_parameters:
            results = results.search(query_parameters.search_parameters)

        if query_parameters.order_parameters:
            results = results.order(query_parameters.order_parameters)

        return results

    def filter_data(self, filter_parameters: FilterParameters) -> ResultSet:
        results: ResultSet = ResultSet(self.users, self.assets)
        return results.filter(filter_parameters)

    def search_data(self, search_parameters: SearchParameters) -> ResultSet:
        results: ResultSet = ResultSet(self.users, self.assets)
        return results.search(search_parameters)

    def order_data(self, order_parameters: OrderParameters) -> ResultSet:
        results: ResultSet = ResultSet(self.users, self.assets)
        return results.order(order_parameters)