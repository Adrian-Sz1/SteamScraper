import PySide6.QtWidgets as qt
from PySide6.QtCore import Qt, QFile, QTextStream, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QFrame)

from modules.helpers.gui.view_helpers import ViewHelpers
from views.basic_view import BasicWindow
from views.widgets.icon_line_edit import IconLineEdit
from views.widgets.view_preferences import ViewPreferences


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.dark_mode = True
        self.dark_mode_btn = None
        self.api_key_icon = None

        self.initialize()

    def initialize(self):
        self.initialize_window_properties()
        #self.initialize_ui()
        self.basic_test_ui()

    def initialize_window_properties(self):
        self.setWindowTitle('Function testbed')
        self.setMinimumSize(640, 480)

        central_widget = qt.QWidget()
        self.setCentralWidget(central_widget)

    def basic_test_ui(self):
        # Define widget here
        main_text = QLabel('Hello world!\nThis is a basic test user interface.')
        main_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        api_key_field = ViewHelpers.create_custom_horizontal_field([QLabel, QLabel('Steam API Key:'), qt.QLineEdit, qt.QPushButton('Validate')])

        # Add widgets to layout here
        self.layout().addChildLayout(api_key_field[0])
        self.layout().addWidget(main_text)


    def initialize_ui(self):

        label = QLabel('Hello world!')
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button = QPushButton('Start')

        start_btn_font = button.font()
        start_btn_font.setPointSize(10)
        start_btn_font.setBold(True)
        button.setFont(start_btn_font)

        layout = qt.QVBoxLayout()

        top_row = self.main_top_row()

        input_view = ViewPreferences()
        top_row.addLayout(input_view)
        top_row.addLayout(self.right_column())


        btm_row = self.main_bottom_row()
        btm_row.addLayout(self.bottom_row())


        layout.addLayout(top_row)
        layout.addLayout(btm_row)

        central_widget.setLayout(layout)

        self.apply_stylesheets("../styles/helper_styles.css",
                               "../styles/dark_mode.qss")

    def apply_stylesheets(self, *filenames):
        combined_styles = ""
        for filename in filenames:
            file = QFile(filename)
            if file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(file)
                combined_styles += stream.readAll()
            else:
                print(f"Failed to load stylesheet: {filename}")
        self.setStyleSheet(combined_styles)

    def load_stylesheet(self, filename):
        file = QFile(filename)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
        else:
            print(f"Failed to load stylesheet: {filename}")

    def main_top_row(self):
        top_row = qt.QHBoxLayout()
        return top_row

    def main_bottom_row(self):
        bottom_row = qt.QHBoxLayout()
        return bottom_row

    def top_row(self):
        bottom_row = qt.QHBoxLayout()
        submit_button = qt.QPushButton('Submit')
        bottom_row.addWidget(submit_button)
        return bottom_row

    def left_column(self):
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Panel)

        left_column = qt.QVBoxLayout()
        left_column.setAlignment(Qt.AlignmentFlag.AlignTop)
        api_key_field_layout = qt.QHBoxLayout()

        self.api_key_icon = QLabel()
        self.api_key_icon.setFixedSize(16, 16)
        self.set_api_key_icon(
            "../icons/xmark.svg"
        )

        icon_line_edit = IconLineEdit('../icons/xmark.svg')

        api_key_field = ViewHelpers.create_custom_horizontal_field([QLabel, QLabel('Steam API Key:'), qt.QLineEdit, qt.QPushButton('Validate')])

        api_key_field_layout.addWidget(self.api_key_icon)

        combo = qt.QComboBox()
        combo.addItems(["Option 1", "Option 2", "Option 3"])

        games_field = ViewHelpers.create_custom_horizontal_field([qt.QLabel('Games'), combo])


        self.dark_mode_btn = qt.QPushButton('Light mode')
        self.dark_mode_btn.clicked.connect(self.toggle_dark_mode)

        input_field = ViewHelpers.create_horizontal_input_field()

        left_column.addWidget(icon_line_edit)
        left_column.addLayout(api_key_field[0])
        left_column.addLayout(input_field[0])
        left_column.addWidget(self.dark_mode_btn)
        left_column.addLayout(api_key_field_layout)
        left_column.addLayout(games_field[0])

        frame.setLayout(left_column)

        #api_key_field[1][2].textChanged.connect(self.validate_api_key)

        return frame



    def right_column(self):
        right_column = qt.QVBoxLayout()
        text_area = qt.QTextEdit()
        text_area.setPlaceholderText('Users, separated, by, a, comma')


        output_frame = QFrame()
        output_frame.setFrameShape(QFrame.Shape.Panel)
        output_frame.setLineWidth(1)
        output_layout = qt.QVBoxLayout()
        output_area = qt.QTextEdit()
        output_area.setPlaceholderText('Output text here')
        output_area.setReadOnly(True)
        output_layout.addWidget(output_area)
        output_frame.setLayout(output_layout)

        right_column.addWidget(text_area)
        right_column.addStretch(1)
        right_column.addWidget(
            qt.QLabel('Output Console')
        )
        right_column.addWidget(output_frame)

        return right_column

    def bottom_row(self):
        bottom_row = qt.QHBoxLayout()
        submit_button = qt.QPushButton('Submit')
        bottom_row.addWidget(submit_button)
        return bottom_row



    def set_api_key_icon(self, icon_path):
        pixmap = QPixmap(icon_path)
        self.api_key_icon.setPixmap(pixmap.scaled(self.api_key_icon.size(), Qt.AspectRatioMode.KeepAspectRatio))

    @Slot()
    def toggle_dark_mode(self):
        if self.dark_mode:
            self.dark_mode_btn.setText('Dark mode')
            self.load_stylesheet("../styles/light_mode.qss")
            self.dark_mode = False
        else:
            self.dark_mode_btn.setText('Light mode')
            self.load_stylesheet("../styles/dark_mode.qss")
            self.dark_mode = True

def main():
    app = QApplication([])

    main_window = BasicWindow()
    main_window.show()

    app.exec()


if __name__ == "__main__":
    main()
