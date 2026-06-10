class InvgateCPU:
    def __init__(self, id, model_name, model, kind, import_uuid, updated_at, family, frequency, cores, manufacturer_id, manufacturer_name, manufacturer_support_url, manufacturer_website_url):
        self.id = id
        self.model_name = model_name
        self.model = model
        self.kind = kind
        self.import_uuid = import_uuid
        self.updated_at = updated_at
        self.family = family
        self.frequency = frequency
        self.cores = cores
        self.manufacturer_id = manufacturer_id
        self.manufacturer_name = manufacturer_name
        self.manufacturer_support_url = manufacturer_support_url
        self.manufacturer_website_url = manufacturer_website_url