import json
import os
from dotenv import load_dotenv
from classes.invgate.invgate_connection import InvgateConnection
from classes.invgate.invgate_routes import InvgateRoutes as routes
from classes.invgate.invgate_user import InvgateUser
from classes.invgate.invgate_computer import InvgateComputer
from classes.invgate.invgate_motherboard import InvgateMotherboard

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
    invgate.populate()
    computer = invgate.get_computer_by_id("964")
    computer.name = "CNBTestEdited"
    computer.print()
    computer.format_type = 1
    computer.lifecycle_status = "In Stock"
    print(computer.to_asset_payload())
    invgate.update_computer(computer)