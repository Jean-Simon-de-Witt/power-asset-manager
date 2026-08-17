# Dependencies
import sys
import os
from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication

# Backend classes
from classes.invgate.invgate_connection import InvgateConnection
from classes.invgate.invgate_routes import InvgateRoutes as routes
from classes.data.data import Data

# Frontend classes
from classes.ui.main_window import MainWindow
# Load Credentials
def main():

    load_dotenv()
    DOMAIN = os.getenv("INVGATE_DOMAIN")
    CLIENT_ID = os.getenv("INVGATE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("INVGATE_CLIENT_SECRET")

    if not all([DOMAIN, CLIENT_ID, CLIENT_SECRET]):
        raise ValueError("Missing API credentials. Check your .env file.")


    invgate = InvgateConnection(DOMAIN, CLIENT_ID, CLIENT_SECRET)

    if not invgate.access_token:
        print("Failed to authenticate with InvGate. Exiting...")
        sys.exit(1)

    app = QApplication(sys.argv) 

    computer = invgate.get_data(endpoint_path = routes.computer(934), v1 = True, query = "include=reported_bios,reported_monitors.specs.manufacturer,reported_printers.specs.manufacturer,reported_storages.specs.manufacturer,reported_rams.specs.manufacturer,reported_cpus.specs.manufacturer,geolocation,osinfo_set.os,osinfo_set.network_adapters,osinfo_set.gateway,osinfo_set.dns,osinfo_set.domains,osinfo_set.osstatus").get("included")
    for dictionary in computer:
        print(f"{dictionary}\n")

if __name__ == "__main__":
    main()     