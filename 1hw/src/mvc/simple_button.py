from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtCore import Slot


@Slot()
def say_hello():
    print("Button clicked, Hello!")


app = QApplication([])
button = QPushButton("Click me")
button.clicked.connect(say_hello)
button.show()
app.exec()