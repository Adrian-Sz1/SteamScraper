from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton


class IconLineEdit(QWidget):
    def __init__(self, icon_path: str = 'icons/checkmark.svg', parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout(self)
        self.line_edit = QLineEdit(self)
        self.button = QPushButton(self)

        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.button)

        if icon_path:
            self.button.setIcon(QIcon(icon_path))

        self.button.setFixedSize(self.button.sizeHint())

        self.apply_styles()

    def apply_styles(self):
        with open('styles/inline_icon_edit.qss', 'r') as file:
            self.setStyleSheet(file.read())