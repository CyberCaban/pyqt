from pathlib import Path
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QSizePolicy, QLayout


def ColWidget(*widgets: QWidget, parent=None):
    m = QWidget(parent=parent)
    l = QVBoxLayout()
    for w in widgets:
        l.addWidget(w)
    m.setLayout(l)
    return m


def RowWidget(*widgets: QWidget, parent=None):
    m = QWidget(parent=parent)
    l = QHBoxLayout()
    for w in widgets:
        l.addWidget(w)
    m.setLayout(l)
    return m


def RowLayout(*widgets: QWidget | QLayout):
    l = QHBoxLayout()
    for w in widgets:
        if isinstance(w, QWidget):
            l.addWidget(w)
        elif isinstance(w, QLayout):
            l.addLayout(w)
    return l


def ColLayout(*widgets: QWidget):
    l = QVBoxLayout()
    for w in widgets:
        if isinstance(w, QWidget):
            l.addWidget(w)
        elif isinstance(w, QLayout):
            l.addLayout(w)
    return l


def find_file(rel_path: str):
    return str(Path(__file__).resolve().parent / rel_path)
