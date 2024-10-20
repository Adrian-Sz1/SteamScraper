from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout


class MainHeader(QVBoxLayout):
    def __init__(self, title:str = 'Default Title', author:str = 'Default Author', parent=None):
        super(MainHeader, self).__init__(parent)
        self.main_layout = QHBoxLayout()

        self.title_label = QLabel(title)
        self.author_label = QLabel(f"By {author}")
        # self.app_icon =
        self.init_ui()


    def init_ui(self):
        left_column = QVBoxLayout()
        right_column = QVBoxLayout()

        custom_font = QFont('Segoe UI Variable Small Semibol', 24, QFont.Weight.Bold)
        self.title_label.setFont(custom_font)
        self.author_label.setFont(QFont('Segoe UI Variable Small', 10, QFont.Weight.Light))
        right_column.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)

        left_column.addWidget(self.title_label)
        right_column.addWidget(self.author_label)

        self.main_layout.addLayout(left_column)
        self.main_layout.addLayout(right_column)

        self.addLayout(self.main_layout)

