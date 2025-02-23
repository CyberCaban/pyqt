from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class FormApp(QWidget):
    def _init_label(self, text, bold=False):
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)
        if bold:
            label.setStyleSheet("font-weight: bold; font-size: 14px;")
        else:
            label.setStyleSheet("font-size: 12px;")
        return label

    def __init__(self):
        super().__init__()
        form_layout = QFormLayout()

        fields = {
            "First name:": QLineEdit(),
            "Last name:": QLineEdit(),
            "Email:": QLineEdit(),
            "Phone:": QLineEdit(),
        }

        for label, field in fields.items():
            form_layout.addRow(label, field)
            setattr(self, label[:-1].lower().replace(" ", "_"), field)

        self.topics = QComboBox()
        self.topics.addItems(["Programming", "Design", "Marketing", "Analytics"])
        self.topics.setEditable(False)
        self.topics.setMaxVisibleItems(4)
        form_layout.addRow("Interests:", self.topics)

        self.data_processing = QCheckBox("Agree to personal data processing")
        self.newsletter = QCheckBox("Agree to newsletter")
        form_layout.addRow(self.data_processing)
        form_layout.addRow(self.newsletter)

        self.validate_btn = QPushButton("Validate")
        self.validate_btn.clicked.connect(self.validate_form)
        form_layout.addRow(self.validate_btn)

        self.setLayout(form_layout)

    def validate_form(self):
        if not all(
            [
                self.first_name.text(),
                self.last_name.text(),
                self.email.text(),
                self.phone.text(),
            ]
        ):
            QMessageBox.warning(self, "Error", "All fields must be filled")
            return

        if not self.data_processing.isChecked():
            QMessageBox.warning(
                self, "Error", "You must agree to personal data processing"
            )
            return
        QMessageBox.information(self, "Success", "Form filled correctly")
