from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from components.Flex import *

products = [
    {"name": "Apples", "price": 50},
    {"name": "Milk", "price": 80},
    {"name": "Bread", "price": 40},
    {"name": "Cheese", "price": 200},
]


class ProductSelector(QWidget):
    def create_product_widgets(self, product):
        checkbox = QCheckBox(product["name"])
        checkbox.stateChanged.connect(self.update_total)

        spinbox = QSpinBox()
        spinbox.setMinimum(1)
        spinbox.setMaximum(100)
        spinbox.valueChanged.connect(self.update_total)

        price_label = QLabel()
        price_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        return {
            "checkbox": checkbox,
            "spinbox": spinbox,
            "price_label": price_label,
            "price": product["price"],
        }

    def __init__(self):
        super().__init__()
        self.total_label = QLabel("Total: 0 .")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Создаем список виджетов с помощью list comprehension
        self.product_widgets = [
            self.create_product_widgets(product) for product in products
        ]

        # Создаем строки с продуктами
        product_rows = [
            RowLayout(widget["checkbox"], widget["spinbox"], widget["price_label"])
            for widget in self.product_widgets
        ]

        # Основной layout
        main_layout = ColLayout(*product_rows, self.total_label)
        self.setLayout(main_layout)
        self.update_total()

    def update_total(self):
        total = 0
        for widget in self.product_widgets:
            if widget["checkbox"].isChecked():
                quantity = widget["spinbox"].value()
                cost = widget["price"] * quantity
                widget["price_label"].setText(f"{cost:.2f}.")
                widget["checkbox"].setStyleSheet("font-weight: bold;")
                total += cost
            else:
                widget["price_label"].setText("")
                widget["checkbox"].setStyleSheet("font-weight: normal;")

        self.total_label.setText(f"Total cost: {total:.2f}.")
