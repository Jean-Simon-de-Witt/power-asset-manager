from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt

class PageHeader(QWidget):
    def __init__(self, title: str, subtitle: str = "", parent = None):
        super().__init__(parent)
        self.title_text = title
        self.subtitle_text = subtitle
        self._setup_ui()

    def _setup_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 15)

        self.text_layout = QVBoxLayout()
        self.text_layout.setSpacing(2)

        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.text_layout.addWidget(self.title_label)

        if self.subtitle_text:
            self.subtitle_label = QLabel(self.subtitle_text)
            self.subtitle_label.setStyleSheet("font-size: 14px; color: gray;")
            self.text_layout.addWidget(self.subtitle_label)

        self.main_layout.addLayout(self.text_layout)

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.main_layout.addItem(spacer)

        self.actions_layout = QHBoxLayout()
        self.actions_layout.setSpacing(10)
        self.actions_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.main_layout.addLayout(self.actions_layout)

    def add_action_button(self, text: str, callback = None) -> QPushButton:
        btn = QPushButton(text)
        btn.setMinimumHeight(30)

        if callback:
            btn.clicked.connect(callback)

        self.actions_layout.addWidget(btn)
        return btn

    def update_title(self, new_title: str):
        self.title_label.setText(new_title)

    def update_subtitle(self, new_subtitle: str):
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.setText(new_subtitle)