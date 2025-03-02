from pathlib import Path
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from components.Comp1 import AgreementDialog
from components.Flex import *


def find_file(rel_path: str):
    return str(Path(__file__).resolve().parent / rel_path)


class RegistrationWizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #3b3b3b; color: white;")
        self.setWindowTitle("Sign Up")
        self.setPage(0, LoginPage())
        self.setPage(1, PersonalInfoPage())
        self.setPage(2, InterestsPage())
        self.setPage(3, AgreementPage())

        self.setOption(QWizard.WizardOption.IndependentPages, True)

    def getRegistrationData(self):
        return {
            "login": self.field("login"),
            "password": self.field("password"),
            "full_name": self.field("full_name"),
            "interests": self.field("interests"),
            "newsletter": self.field("newsletter"),
            "agreement": self.field("agreement"),
        }


class LoginPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Login and password")

        self.loginEdit = QLineEdit()
        self.loginEdit.setPlaceholderText("Enter login")
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setPlaceholderText("Enter password")
        self.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.setLayout(
            ColLayout(
                QLabel("Login:"), self.loginEdit, QLabel("Password:"), self.passwordEdit
            )
        )

        self.registerField("login*", self.loginEdit)
        self.registerField("password*", self.passwordEdit)


class PersonalInfoPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Personal info")

        layout = QVBoxLayout()
        self.fullNameEdit = QLineEdit()
        self.fullNameEdit.setPlaceholderText("Enter Full Name")

        layout.addWidget(QLabel("Full Name:"))
        layout.addWidget(self.fullNameEdit)
        self.setLayout(layout)

        self.registerField("full_name*", self.fullNameEdit)


class InterestsPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Interests and newsletter")

        layout = QVBoxLayout()
        self.interestsList = QListWidget()
        self.interestsList.addItems(
            ["Programming", "Design", "Marketing", "Product Management"]
        )
        self.interestsList.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

        self.newsletterCheck = QCheckBox("Agree to newsletter")

        layout.addWidget(QLabel("Choose your favorite topics:"))
        layout.addWidget(self.interestsList)
        layout.addWidget(self.newsletterCheck)
        self.setLayout(layout)

        self.registerField("newsletter", self.newsletterCheck)

    def validatePage(self):
        selected_items = [item.text() for item in self.interestsList.selectedItems()]
        self.wizard().setProperty("interests", selected_items)
        return super().validatePage()


class AgreementPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("License agreement")

        self.button = QPushButton("Open Dialog", self)
        self.button.clicked.connect(self.show_dialog)

        self.status_label = QLabel(self)
        self.agreementCheck = QCheckBox()
        self.agreementCheck.setEnabled(False)

        self.setLayout(ColLayout(self.button, self.status_label))

        self.registerField("agreement", self.agreementCheck)

    def show_dialog(self):
        dialog = AgreementDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            status = dialog.is_agreed()
            self.status_label.setText(
                "Agreement accepted" if status else "Agreement not accepted"
            )
            self.agreementCheck.setChecked(status)


class RegistrationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.registerButton = QPushButton("Sign up")
        self.registerButton.clicked.connect(self.showRegistration)

        self.infoLabel = QLabel("Registration info will be displayed here")

        self.setLayout(ColLayout(self.registerButton, self.infoLabel))

    def showRegistration(self):
        wizard = RegistrationWizard(self)
        if wizard.exec() == QWizard.DialogCode.Accepted:
            data = wizard.getRegistrationData()
            interests = wizard.property("interests")
            print(data, interests)
            info = (
                f"Login: {data['login']}\n"
                f"Full name: {data['full_name']}\n"
                f"Topics: {', '.join(interests)}\n"
                f"Newsletter: {'Да' if data['newsletter'] else 'Нет'}\n"
                f"Agreement: {'Принято' if data['agreement'] else 'Не принято'}"
            )
            self.infoLabel.setText(info)
