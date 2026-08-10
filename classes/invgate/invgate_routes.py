class InvgateRoutes:    
    def users():
        return "/public-api/v2/people/"

    def users_detail():
        return "/public-api/v2/people/detail/"
    
    def user(id):
        return f"/public-api/v2/people/{id}/"
    
    def financials():
        return "/public-api/v2/finance/"
    
    def financial(id):
        return f"/public-api/v2/finance/{id}/"
    
    def assets():
        return "/public-api/v2/assets-lite/"
    
    def asset(id):
        return f"/public-api/v2/assets-lite/{id}/"

    def vendors():
        return "/public-api/v2/vendors/"

    def vendor(id):
        return f"/public-api/v2/vendors/{id}/"
    
    def tags():
        return "/public-api/v2/tags/"

    def tag(id):
        return f"/public-api/v2/tags/{id}/"

    def purchase_orders():
        return "/public-api/v2/purchase-orders/"

    def purchase_order(id):
        return f"/public-api/v2/purchase-orders/{id}/"

    def manufacturers():
        return "/public-api/v2/manufacturers/"

    def manufacturer(id):
        return f"/public-api/v2/manufacturers/{id}/"

    def healths():
        return "/public-api/v2/health/"

    def health(computer_id):
        return f"/public-api/v2/health/{computer_id}/"

    # This is an API version 1 route. v1 must be set to true when using this path with get_data.
    def locations():
        return "/public-api/locations/"

    # This is an API version 1 route. v1 must be set to true when using this path with get_data.
    def location(id):
        return f"/public-api/locations/{id}/"

    # This is an API version 1 route. v1 must be set to true when using this path with get_data.
    def status():
        return "/public-api/asset-status/"

    def software(id):
        return f"/public-api/v2/installed-software/{id}/"

    def softwares():
        return "/public-api/v2/installed-software/"

    def operating_system_update(id):
        return f"/public-api/v2/os-updates/{id}/"

    def operating_system_updates():
        return "/public-api/v2/os-updates/"