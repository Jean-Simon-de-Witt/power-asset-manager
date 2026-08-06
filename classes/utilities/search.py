from classes.invgate.invgate_connection import InvgateConnection
from classes.invgate.invgate_asset import InvgateAsset
from classes.invgate.invgate_user import InvgateUser

class Search:
    def __init__(self, term: str = None, filters: list[FilterParameters] = None, ordering: str = None, options: dict = None):
        self.tags: list = term.split()
        self.filter: dict = filter
        self.ordering: dict = ordering
        self.options: dict = options

class FilterParameters:
    def __init__(self, field: str, expression: str, value):
        self.field = field
        self.expression = expression
        self.value = value

    def compare(self, value) -> bool:
        if self.expression == "equals":
            return value == self.value
        if self.expression == "greater_than" or self.expression == "after":
            return value > self.value
        if self.expression == "lesser_than" or self.expression == "before":
            return value < self.value
        if self.expression == "not_equal_to":
            return value != self.value
        if self.expression == "greater_than_or_equal":
            return value >= self.value
        if self.expression == "lesser_than_or_equal":
            return value <= self.value
        if self.expression == "is_empty":
            return value is None
        if self.expression == "is_not_empty":
            return value is not None
        return None

class Results:
    def __init__(self, connection: InvgateConnection = None, result_set: dict = None):
        if connection and result_set:
            if result_set.get("users"):
                self.users: list[InvgateUser] = result_set.get("users")
            if result_set.get("assets"):
                self.assets: list[InvgateAsset] = result_set.get("assets")
        elif result_set:
            if result_set.get("users"):
                self.users: list[InvgateUser] = result_set.get("users")
            if result_set.get("assets"):
                self.assets: list[InvgateUser] = result_set.get("assets")

        elif connection:
            response = connection.load_data(include_users = True, include_assets = True)
            self.users: list[InvgateUser] = response.get("users")
            self.assets: list[InvgateAsset] = response.get("assets")
        else:
            return None

    def search(self, search: Search):
        results = {}
        if search.options.get("include").get("assets"):
            results["assets"] = []
            fields = search.options.get("include").get("assets").get("fields")
            for tag in search.tags:
                for asset in self.assets:
                    asset_match = asset.search(tag = tag, fields = fields)
                    if asset_match.get("status"):
                        results["assets"].append({"asset": asset, "matched_field": asset_match.get("field")})

        if search.options.get("include").get("users"):
            results["users"] = []
            fields = search.options.get("include").get("users").get("fields")

            for tag in search.tags:
                for user in self.users:
                    user_match = user.search(tag = tag, fields = fields)
                    if user_match.get("status"):
                        results["users"].append({"user": user, "matched_field": user_match.get("field")})

        return results