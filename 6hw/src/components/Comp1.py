from pathlib import Path
from PyQt6.QtWidgets import (
    QPushButton,
    QDialog,
    QCheckBox,
    QLabel,
    QWidget,
    QTextBrowser,
)
from components.Flex import *
from PyQt6.QtCore import QFile, QIODevice


def find_file(rel_path: str):
    return str(Path(__file__).resolve().parent / rel_path)


class AgreementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("License Agreement")

        eula_file = QFile(find_file("../public/EULA.md"))
        if eula_file.open(
            QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text
        ):
            eula_content = str(eula_file.readAll(), "utf-8")
            eula_file.close()
        else:
            eula_content = "Failed to load the license agreement."

        self.text_browser = QTextBrowser(self)
        self.text_browser.setMarkdown(eula_content)
        self.checkbox = QCheckBox("I agree", self)
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)

        layout = ColLayout(self.text_browser, self.checkbox, self.ok_button)
        self.setLayout(layout)

    def is_agreed(self):
        return self.checkbox.isChecked()


class EULA(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Open Dialog", self)
        self.button.clicked.connect(self.show_dialog)

        self.status_label = QLabel(self)
        self.setLayout(ColLayout(self.button, self.status_label))

    def show_dialog(self):
        dialog = AgreementDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            status = (
                "Agreement accepted" if dialog.is_agreed() else "Agreement not accepted"
            )
            self.status_label.setText(status)
