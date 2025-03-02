from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableView,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QLabel,
    QFormLayout,
    QMessageBox,
)
from models.Product import Product
from components.Flex import *


class ProductModel(QAbstractTableModel):
    def __init__(self, products=None):
        super().__init__()
        self.products = products or []
        self.headers = ["Name", "Quantity", "Unit Weight (kg)", "Total Weight (kg)"]

    def rowCount(self, parent=QModelIndex()):
        return len(self.products)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        product = self.products[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            return [
                product.name,
                str(product.quantity),
                f"{product.unit_weight:.2f}",
                f"{product.total_weight:.2f}",
            ][index.column()]
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientation == Qt.Orientation.Horizontal
        ):
            return self.headers[section]
        return None

    def add_product(self, product):
        if not product.name.strip():
            return False

        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.products.append(product)
        self.endInsertRows()
        return True

    def total_weight(self):
        return sum(p.total_weight for p in self.products)


class ProductApp(QWidget):
    def __init__(self):
        super().__init__()

        self.model = ProductModel()
        self.view = QTableView()
        self.view.setModel(self.model)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter product name...")
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(9999)
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setMinimum(0.01)
        self.weight_input.setMaximum(9999.99)
        self.weight_input.setDecimals(3)
        self.add_button = QPushButton("Add Product")
        self.add_button.clicked.connect(self.add_product)

        self.total_label = QLabel("Total Weight: 0.00 kg")

        form = QFormLayout()
        form.addRow("Product Name:", self.name_input)
        form.addRow("Quantity:", self.quantity_input)
        form.addRow("Unit Weight (kg):", self.weight_input)
        form.addRow(self.add_button)

        layout = ColLayout(form, self.view, self.total_label)
        self.setLayout(layout)

    def add_product(self):
        product = Product(
            name=self.name_input.text(),
            quantity=self.quantity_input.value(),
            unit_weight=self.weight_input.value(),
        )

        if self.model.add_product(product):
            self.name_input.clear()
            self.quantity_input.setValue(1)
            self.weight_input.setValue(0.01)
            self.total_label.setText(
                f"Total Weight: {self.model.total_weight():.3f} kg"
            )
        else:
            QMessageBox.warning(self, "Invalid Product", "Product name cannot be empty")
