import json
import os
from dotenv import load_dotenv
from classes.invgate_connection import InvgateConnection
from classes.invgate_routes import InvgateRoutes as routes

# Load Credentials
load_dotenv()

DOMAIN = os.getenv("INVGATE_DOMAIN")
CLIENT_ID = os.getenv("INVGATE_CLIENT_ID")
CLIENT_SECRET = os.getenv("INVGATE_CLIENT_SECRET")

if not all([DOMAIN, CLIENT_ID, CLIENT_SECRET]):
    raise ValueError("Missing API credentials. Check your .env file.")


invgate = InvgateConnection(DOMAIN, CLIENT_ID, CLIENT_SECRET)

if invgate.access_token:
    print("Fetching data...")

    response_data = invgate.get_user(888)

    if response_data:
        print(json.dumps(response_data, indent=4))