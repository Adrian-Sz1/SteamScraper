from PySide6.QtWidgets import QLayout, QFrame, QVBoxLayout, QLabel, QLineEdit, QPushButton


class ViewPreferences(QLayout):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.api_key_element = None
        self.initialize()

    def initialize(self):
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Panel)

        self.main_layout = QVBoxLayout()

        # Example Widgets
        self.api_key_label = QLabel("API Key:")
        self.api_key_input = QLineEdit()
        self.save_button = QPushButton("Save")

        # Add widgets to the layout
        self.main_layout.addWidget(self.api_key_label)
        self.main_layout.addWidget(self.api_key_input)
        self.main_layout.addWidget(self.save_button)

        self.frame.setLayout(self.main_layout)

        self.addWidget(self.frame)

    def addItem(self, item):
        pass  # Implementation required for abstract method

    def count(self):
        return self.main_layout.count()

    def itemAt(self, index):
        return self.main_layout.itemAt(index)

    def takeAt(self, index):
        return self.main_layout.takeAt(index)

    def addWidget(self, widget):
        self.main_layout.addWidget(widget)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        if self.frame:
            self.frame.setGeometry(rect)

    def sizeHint(self):
        return self.frame.sizeHint()
