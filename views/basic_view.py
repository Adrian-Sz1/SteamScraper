from PySide6.QtCore import Qt, Slot, QFile, QTextStream
from PySide6.QtWidgets import (QMainWindow, QWidget, QLabel,
                               QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit)

from modules.helpers.gui.view_helpers import ViewHelpers
from viewmodels.api_handler_viewmodel import ApiHandlerViewModel
from viewmodels.config_viewmodel import ConfigViewModel
from viewmodels.settings_viewmodel import SettingsViewModel
from views.widgets.api_key_input_field import ApiKeyField
from views.widgets.app_status_bar import AppStatusBar
from views.widgets.main_header import MainHeader


class BasicWindow(QMainWindow):
    def __init__(self):
        super(BasicWindow, self).__init__()
        self.config_vm = ConfigViewModel()
        self.api_vm = ApiHandlerViewModel()
        self.settings_vm = SettingsViewModel(self.config_vm.root_directory)

        self.dark_mode = False
        self.dark_mode_btn = None
        self.api_key_icon = None
        self.api_key_input = None

        self.header_title_element = None
        self.status_bar = AppStatusBar(
            current_theme='Light Mode',
            build_version=self.config_vm.build_version,
            author_name=self.config_vm.author)

        self.central_widget = None
        self.initialize()

        self.toggle_dark_mode()

    def initialize(self):
        self.initialize_window_properties()
        self.basic_test_ui()

    def initialize_window_properties(self):
        self.setWindowTitle('Basic GUI')
        self.setMinimumSize(640, 480)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

    def basic_test_ui(self):
        main_layout = QVBoxLayout()

        # region HEADER ROW
        header_row = QVBoxLayout()

        self.header_title_element = MainHeader(self.config_vm.app_name, self.config_vm.author)
        header_row.addLayout(self.header_title_element)

        # Horizontal Line Separator
        header_row.addWidget(ViewHelpers.create_horizontal_separator())

        header_widget = QWidget()
        header_widget.setLayout(header_row)

        main_layout.addWidget(header_widget)
        main_layout.setAlignment(header_widget, Qt.AlignmentFlag.AlignTop)
        # endregion
        # region BODY ROW
        body_row = QHBoxLayout()

        # region LEFT BODY COLUMN
        left_body_column = QVBoxLayout()
        field_layout = QHBoxLayout()
        

        self.api_key_input = ApiKeyField(self.api_vm, self.settings_vm)
        left_body_column.addWidget(self.api_key_input)



        field_layout = QHBoxLayout()
        self.save_prefs_btn = QPushButton('Save Preferences')
        self.save_prefs_btn.clicked.connect(self.save_preferences)
        field_layout.addWidget(self.save_prefs_btn)
        left_body_column.addLayout(field_layout)
        body_row.addLayout(left_body_column)

        body_row.addWidget(ViewHelpers.create_vertical_separator())
        # endregion
        # region RIGHT BODY COLUMN
        right_body_column = QVBoxLayout()
        right_body_column.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_text = QLabel('Hello world!\n'
                           'This is a basic test user interface.\n'
                           'Change the theme with the button below\n|\n|\n\\/')
        main_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.dark_mode_btn = QPushButton('Change Theme')
        self.dark_mode_btn.clicked.connect(self.toggle_dark_mode)
        right_body_column.addWidget(main_text)
        right_body_column.addWidget(self.dark_mode_btn)

        body_row.addLayout(right_body_column)

        main_layout.addLayout(body_row)
        # endregion
        # endregion
        # region FOOTER ROW
        footer_row = QHBoxLayout()


        main_layout.addLayout(footer_row)
        # endregion

        self.setStatusBar(self.status_bar)

        self.central_widget.setLayout(main_layout)

    def toggle_show_api_key(self):
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Normal) if self.api_key_input.echoMode() == QLineEdit.EchoMode.Password else self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)

    @Slot()
    def toggle_dark_mode(self):
        if self.dark_mode:
            self.dark_mode_btn.setText('Switch to Dark mode')
            self.status_bar.set_theme('Light mode')
            self.load_stylesheet("styles/light_mode.qss")
            self.dark_mode = False
        else:
            self.dark_mode_btn.setText('Switch to Light mode')
            self.status_bar.set_theme('Dark mode')
            self.load_stylesheet("styles/dark_mode.qss")
            self.dark_mode = True

    def save_preferences(self):
        pass

    def load_stylesheet(self, filename):
        file = QFile(filename)
        if not file.exists():
            print(f"Stylesheet file {filename} does not exist")
            return
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
        else:
            print(f"Failed to load stylesheet: {filename}")
