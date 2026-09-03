from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit, QPushButton, QLabel, QFrame
from PyQt6.QtCore import pyqtSignal, Qt

class FilterRow(QWidget):
    remove_requested = pyqtSignal(QWidget)

    def __init__(self, available_fields: list[str], parent = None):
        super().__init__(parent)
        self.available_fields = available_fields
        self._setup_ui()

    def _setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)

        self.field_combo = QComboBox()
        self.field_combo.addItems(self.available_fields)

        self.operator_combo = QComboBox()
        self.operator_combo.addItems("equals", "not equal to", "contains", "greater than", "lesser than")

        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Value...")

        self.remove_btn = QPushButton("X")
        self.remove_btn.setFixedWidth(30)

        self.remove_btn.clicked.connect(lambda: self.remove_requested.emit(self))

        self.layout.addWidget(self.field_combo)
        self.layout.addWidget(self.operator_combo)
        self.layout.addWidget(self.value_input)
        self.layout.addWidget(self.remove_btn)

    def get_condition(self) -> dict:
        return {
            "field": self.field_combo.currentText(),
            "operator": self.operator_combo.currentText(),
            "value": self.value_input.text().strip()
        }

class FilterPanel(QFrame):

    filters_applied = pyqtSignal(list)

    def __init__(self, fields: list[str] = None, parent = None):
        super().__init__(parent)

        self.setFrameShape(QFrame.Shape.StyledPanel)

        self.fields = fields or ["ID", "Name", "Serial", "Status", "IP Address"]
        self.filter_rows: list[FilterRow] = []
        self._setup_ui()

    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)

        self.title_label = QLabel("<b>Advanced Filters</b>")
        self.main_layout.addWidget(self.title_label)

        self.rows_container = QWidget()
        self.rows_layout = QVBoxLayout(self.rows_container)
        self.rows_layout.setContentsMargins(0, 0, 0, 0)
        self.rows_layout.addWidget(self.rows_container)

        self.btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Add Condition")
        self.clear_btn = QPushButton("Clear All")
        self.apply_btn = QPushButton("Apply Filters")

        self.apply_btn.setDefault(True)

        self.btn_layout.addWidget(self.add_btn)
        self.btn_layout.addWidget(self.clear_btn)
        self.btn_layout.addWidget(self.apply_btn)

        self.main_layout.addLayout(self.btn_layout)

        self.add_btn.clicked.connect(self.add_filter_row)
        self.clear_btn.clicked.connect(self.clear_all_rows)
        self.apply_btn.clicked.connect(self.compile_and_emit_filters)

        self.add_filter_row()

    def add_filter_row(self):
        row = FilterRow(available_fields = self.fields)
        row.remove_requested.connect(self.filter_row)

        self.rows_layout.addWidget(row)
        self.filter_rows.append(row)

    def remove_filter_row(self, row_widget: FilterRow):

        if row_widget in self.filter_rows:
            self.filter_rows.remove(row_widget)
            self.rows_layout.removeWidget(row_widget)
            row_widget.deleteLater()

    def clear_all_rows(self):
        for row in reversed(self.filter_rows):
            self.remove_filter_row(row)

        self.filters_applied.emit([])

    def compile_and_emit_filters(self):
        conditions = []
        for row in self.filter_rows:
            condition = row.get_condition()

            if condition["value"]:
                conditions.append(condition)

        self.filters_applied.emit(conditions)