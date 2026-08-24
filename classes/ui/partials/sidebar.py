from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import pyqtSignal

class Sidebar(QWidget):
    page_changed = pyqtSignal(str)
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self._setup_ui()
        
    def _setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 15, 10, 15)
        self.layout.setSpacing(10)
        
        self.title = QLabel("Power Asset Manager")
        self.layout.addWidget(self.title)
        
        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_assets = QPushButton("Assets")
        self.btn_users = QPushButton("Advanced Search")
        self.btn_settings = QPushButton("Settings")
        
        self.btn_dashboard.clicked.connect(lambda: self.page_changed.emit("dashboard"))
        self.btn_assets.clicked.connect(lambda: self.page_changed.emit("assets"))
        self.btn_users.clicked.connect(lambda: self.page_changed.emit("advanced_search"))
        self.btn_settings.clicked.connect(lambda: self.page_changed.emit("settings"))
        
        self.layout.addWidget(self.btn_dashboard)
        self.layout.addWidget(self.btn_assets)
        self.layout.addWidget(self.btn_users)
        self.layout.addWidget(self.btn_settings)
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addItem(spacer)