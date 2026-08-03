import json
import os
from dotenv import load_dotenv
from classes.invgate.invgate_connection import InvgateConnection
from classes.invgate.invgate_routes import InvgateRoutes as routes
from classes.invgate.invgate_user import InvgateUser
from classes.invgate.invgate_asset import InvgateAsset

# Load Credentials
load_dotenv()

DOMAIN = os.getenv("INVGATE_DOMAIN")
CLIENT_ID = os.getenv("INVGATE_CLIENT_ID")
CLIENT_SECRET = os.getenv("INVGATE_CLIENT_SECRET")

if not all([DOMAIN, CLIENT_ID, CLIENT_SECRET]):
    raise ValueError("Missing API credentials. Check your .env file.")


invgate = InvgateConnection(DOMAIN, CLIENT_ID, CLIENT_SECRET)

if invgate.access_token:
    cnbtest = invgate.get_asset_with_collections(name = "CNBTestEdited")

    cnbtest.name = "CNBTest"
    cnbtest.format = "desktop"
    print(cnbtest.to_json(include_id = True))
    invgate.patch_data(routes.asset(cnbtest.id), cnbtest.to_json(include_id = True))



        