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
from classes.ui.windows.main_window import MainWindow
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
    asset = invgate.get_asset(name = "CNB1773")
    print(invgate.get_computer(asset).to_string())
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()     