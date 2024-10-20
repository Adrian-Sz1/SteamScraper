from typing import Tuple, Type, List, Union

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget


class ViewHelpers:

    @staticmethod
    def create_horizontal_input_field() -> Tuple[QHBoxLayout, QLabel, QLineEdit, QPushButton]:
        field_layout = QHBoxLayout()
        field_label = QLabel('Input Field')
        field_line_edit = QLineEdit()
        field_submit_btn = QPushButton('Submit')

        field_layout.addWidget(field_label)
        field_layout.addWidget(field_line_edit)
        field_layout.addWidget(field_submit_btn)

        return field_layout, field_label, field_line_edit, field_submit_btn

    @staticmethod
    def create_custom_horizontal_field(widget_types: List[Union[Type[QWidget], QWidget]]) -> Tuple[QHBoxLayout, list[QWidget]]:
        """
            Creates a horizontal field with the given widgets.
        Args:
            widget_types: A list containing either QWidget instances or QWidget classes.

        Returns:
            A tuple where the first element is a QHBoxLayout containing the widgets,
            and the second element is a list of QWidget instances.
        """
        field_layout = QHBoxLayout()

        widget_instances = []
        for widget in widget_types:
            if isinstance(widget, QWidget):
                widget_instances.append(widget)
            else:
                widget_instances.append(widget())

        for widget_instance in widget_instances:
            field_layout.addWidget(widget_instance)

        return field_layout, widget_instances

    @staticmethod
    def create_horizontal_separator() -> QFrame:
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        return separator

    @staticmethod
    def create_vertical_separator() -> QFrame:
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        return separator