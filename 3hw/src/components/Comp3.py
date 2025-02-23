from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from components.Flex import *


class AgeCalc(QWidget):
    def __init__(self):
        super().__init__()
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.dateChanged.connect(self.calculate_age)
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout = ColLayout(self.date_edit, self.result_text)
        self.setLayout(layout)
        self.calculate_age()

    def calculate_age(self):
        birth_date = self.date_edit.date()
        current_date = QDate.currentDate()
        current_datetime = QDateTime.currentDateTime()
        years = current_date.year() - birth_date.year()
        if current_date.month() < birth_date.month() or (
            current_date.month() == birth_date.month()
            and current_date.day() < birth_date.day()
        ):
            years -= 1
        birth_datetime = QDateTime(birth_date, QTime(0, 0))
        seconds = birth_datetime.secsTo(current_datetime)
        hours = seconds // 3600
        result = f"<h2>Age:</h2>"
        result += f"<p><b>Years:</b> {years}</p>"
        result += f"<p><b>Hours:</b> {hours:,}</p>"
        result += f"<p><b>Seconds:</b> {seconds:,}</p>"

        self.result_text.setHtml(result)
