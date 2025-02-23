from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class ScheduleApp(QWidget):
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
        grid = QGridLayout()
        self.setLayout(grid)
        days = ["Понедельник", "Вторник", "Среда"]
        for row, day in enumerate(days, start=1):
            grid.addWidget(self._init_label(day, bold=True), 0, row)

        times = ["9:00", "11:00", "13:00", "15:00"]
        for col, time in enumerate(times, start=1):
            grid.addWidget(self._init_label(time, bold=True), col, 0)

        schedule = [
            [
                "Дифференциальные уравнения",
                "Языки и методы программирования",
                "Языки и методы программирования\nОсновы тестирования ПО (практика)",
            ],
            [
                "Программирование для .NET Framework",
                "Программирование для .NET Framework",
                "Теория вероятностей и математическая статистика",
            ],
            [
                "Компьютерные сети/\nАлгоритмы и анализ сложности",
                "Алгоритмы и анализ сложности/\nКомпьютерные сети",
                "Дифференциальные уравнения",
                "Социальные и этические вопросы информатизации",
            ],
        ]

        for col, subjects in enumerate(schedule, start=1):
            for row, subject in enumerate(subjects, start=1):
                grid.addWidget(self._init_label(subject), row, col)
