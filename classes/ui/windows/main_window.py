from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from classes.ui.partials.sidebar import Sidebar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Power Asset Manager")
        self.resize(1200, 800)

        self.pages = {}

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.sidebar = Sidebar()

        self.page_router = QStackedWidget()
        self.main_layout.addWidget(self.page_router, stretch = 1)

        self._initialise_pages()

    def _initialise_pages(self):

        self.pages["dashboard"] = self._create_placeholder_page("Dashboard View")
        self.pages["assets"] = self._create_placeholder_page("Assets Management View")
        self.pages["advanced_search"] = self._create_placeholder_page("Advanced Search View")
        self.pages["settings"] = self._create_placeholder_page("Settings View")

    def _connect_signals(self):
        self.sidebar.page_changed.connect(self.switch_page)

    def switch_page(self, page_name: str):
        if page_name in self.pages:
            target_widget = self.pages[page_name]
            self.page_router.setCurrentWidget(target_widget)
        else:
            print(f"Routing Error: Page '{page_name}' does not exist.")

    def _create_placeholder_page(self, text: str) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 24px; color: white;")
        layout.addWidget(label)
        return page