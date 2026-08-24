from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSignal

class SearchBar(QWidget):
    search_submitted = pyqtSignal(str)
    search_cleared = pyqtSignal()
    
    def __init__(self, placeholder: str = "Search...", parent = None):
        super().__init__(parent)
        self.placeholder = placeholder
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(self.placeholder)
        self.input_field.setClearButtonEnabled(True)
        
        self.search_button = QPushButton("Search")
        self.clear_button = QPushButton("Clear")
        
        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.clear_button)
        
    def _connect_signals(self):
        self.search_button.clicked.connect(self._handle_search)
        self.input_field.returnPressed.connect(self._handle_search)
        
        self.clear_button.clicked.connect(self._handle_clear)
        
    def _handle_search(self):
        query = self.input_field.text().strip()
        self.search_submitted.emit(query)
        
    def _handle_clear(self):
        self.input_field.clear()
        self.search_cleared.emit()
        
    def get_text(self) -> str:
        return self.input_field.text().strip()
    
    def set_text(self, text: str):
        self.input_field.setText(text)