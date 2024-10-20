from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QLineEdit, QHBoxLayout

from viewmodels.api_handler_viewmodel import ApiHandlerViewModel
from viewmodels.settings_viewmodel import SettingsViewModel


class ApiKeyField(QWidget):
    apiKeyChanged = Signal(str)
    validatePressed = Signal(str)

    def __init__(self, api_handler_viewmodel: ApiHandlerViewModel, settings_viewmodel: SettingsViewModel, parent=None):
        super().__init__(parent)
        self.api_vm = api_handler_viewmodel
        self.settings_vm = settings_viewmodel

        self.label = QLabel('Steam Api Key:')
        label_font = self.label.font()
        label_font.setBold(True)
        self.label.setFont(label_font)


        self.input_field = QLineEdit(self.settings_vm.steam_api_key)
        self.input_field.setMaxLength(32)
        self.input_field.setPlaceholderText('Your Api key here...')
        self.show_btn = QPushButton('Show')
        self.validate_btn = QPushButton('Validate')

        self.input_field.setEchoMode(QLineEdit.EchoMode.Password) # Set to hide contents by default

        self.input_field.textChanged.connect(self.on_input_changed)
        self.api_vm.apiKeyChanged.connect(self.set_api_key)
        self.apiKeyChanged.connect(self.api_vm.test)

        self.on_input_changed(self.settings_vm.steam_api_key)

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.show_btn)
        layout.addWidget(self.validate_btn)

        self.setLayout(layout)

        self.show_btn.clicked.connect(self.toggle_visibility)

        self.validate_btn.clicked.connect(self.validate_api_key)
        self.api_vm.apiValidationStatusChanged.connect(self.change_validation_status)
        self.validatePressed.connect(self.api_vm.validate_api_key)

    def toggle_visibility(self):
        if self.input_field.echoMode() == QLineEdit.EchoMode.Password:
            self.input_field.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_btn.setText("Hide")
        else:
            self.input_field.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_btn.setText("Show")

    def on_input_changed(self, text):
        self.apiKeyChanged.emit(text)

        self.validate_btn.setText('Validate')
        self.validate_btn.setFont(self.validate_btn.font())
        self.validate_btn.setDisabled(False)
        self.validate_btn.setStyleSheet(
            'QPushButton {color: black;}'
        )

    def get_api_key(self):
        return self.input_field.text()

    def set_api_key(self, api_key):
        self.input_field.setText(api_key)

    def change_validation_status(self, result):
        if result:
            self.validate_btn.setText('Valid')
            self.validate_btn.setFont(self.validate_btn.font())
            self.validate_btn.setDisabled(True)
            self.validate_btn.setStyleSheet(
                'QPushButton {color: lime;}'
            )
        else:
            self.validate_btn.setText('Invalid')
            self.validate_btn.setFont(self.validate_btn.font())
            self.validate_btn.setDisabled(True)
            self.validate_btn.setStyleSheet(
                'QPushButton {color: red;}'
            )

    def validate_api_key(self):
        self.validatePressed.emit(self.input_field.text())
