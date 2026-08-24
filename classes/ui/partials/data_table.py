from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableView, QAbstractItemView
from PyQt6.QtCore import Qt, QAbstractTableModel

class GenericTableModel(QAbstractTableModel):
    def __init__(self, data: list[list[str]], headers: list[str]):
        super().__init__()
        self._data = data
        self._headers = headers
        
    def rowCount(self, parent = None) -> int:
        return len(self._data)
    
    def columnCount(self, parent = None) -> int:
        return len(self._headers)
    
    def data(self, index, role = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            col = index.column
            
            return str(self._data[row][col])
        return None
    
    def headerData(self, section, orientation, role = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        return None
    
    def update_data(self, new_data: list[list[str]], new_headers: list[str] = None):
        self.beginResetModel()
        self._data = new_data
        if new_headers:
            self._headers = new_headers
        self.endResetModel()
        
class DataTable(QWidget):
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self._setup_ui()
        
    def _setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.table_view = QTableView()
        
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        
        header = self.table_view.horizontalHeader()
        header.setStretchLastSection(True)
        
        self.model = GenericTableModel(data=[], headers = [])
        self.table_view.setModel(self.model)
        
        self.layout.addWidget(self.table_view)
        
    def load_data(self, headers: list[str], rows: list[list[str]]):
        self.model.update_data(rows, headers)
        self.table_view.resizeColumnsToContents()