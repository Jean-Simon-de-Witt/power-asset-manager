class InvgateRoutes:
    def computers():
        return "/public-api/computers/"
    
    def computers_all_attributes():
        return "/public-api/computers/?include=reported_motherboard.specs.manufacturer,reported_cpus.specs.manufacturer,reported_rams.specs.manufacturer"
    
    def computer(id):
        return f"/public-api/computers/{id}/"
    
    def computer_motherboard(id):
        return f"/public-api/computers/{id}?include=reported_motherboard.specs.manufacturer"
    
    def computer_cpu(id):
        return f"/public-api/computers/{id}?include=reported_cpus.specs.manufacturer"
    
    def computer_ram(id):
        return f"/public-api/computers/{id}?include=reported_rams.specs.manufacturer"
    
    def users():
        return "/public-api/people/"
    
    def user(id):
        return f"/public-api/people/{id}/"
    
    def locations():
        return "/public-api/locations/"
    
    def location(id):
        return f"/public-api/locations/{id}/"
    
    def tags():
        return "public-api/tags/"
    
    def tag(id):
        return f"public-api/tags/{id}/"
    
    def financials():
        return "public-api/finance/"
    
    def financial(id):
        return f"public-api/finance/{id}/"
    
    def software(id):
        return f"public-api/installed-software/{id}/"