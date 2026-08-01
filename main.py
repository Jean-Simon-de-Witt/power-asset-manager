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
    os_updates = invgate.get_operating_system_updates_for_computer(934).get("operating_system_updates")

    for os_update in os_updates:
        print(os_update.to_string())
        