from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt
from classes.ui.partials.sidebar import Sidebar

class MainWindow(QMainWindow):
    def __init__(self, connection):
        super().__init__()

        self.connection = connection

        self.setWindowTitle("Power Asset Manager")
        self.resize(400, 200)

        layout = QVBoxLayout()
        self.sidebar = Sidebar()
        self.header_actions = QHBoxLayout()
        layout.addWidget(self.sidebar)
        
        self.file_button = QPushButton("File")
        self.edit_button = QPushButton("Edit")

        self.file_button.setStyleSheet("background-color: transparent; border: none;")

        self.header_actions.addWidget(self.file_button)
        self.header_actions.addWidget(self.edit_button)


        self.status_label = QLabel("Ready.", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.test_button = QPushButton("Test API")
        self.test_button.clicked.connect(self.run_api_test)

        layout.addLayout(self.header_actions)
        layout.addWidget(self.status_label)
        layout.addWidget(self.test_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def run_api_test(self):
        self.status_label.setText("Fetching user...")

        test_user = self.connection.get_user(id = 46)

        if test_user:
            self.status_label.setText(f"Success! Found: {test_user.name}")
        else:
            self.status_label.setText("User not found or API error.")