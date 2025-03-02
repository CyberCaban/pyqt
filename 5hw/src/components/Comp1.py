from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QListView,
    QMessageBox,
)


class NoteModel(QAbstractListModel):
    def __init__(self, notes=None):
        super().__init__()
        self.notes = notes or []

    def rowCount(self, parent=QModelIndex()):
        return len(self.notes)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            return self.notes[index.row()]
        return None

    def add_note(self, note):
        if not note or not note.strip():
            return False

        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.notes.append(note)
        self.endInsertRows()
        return True

    def remove_note(self, index):
        if not index.isValid():
            return False

        self.beginRemoveRows(QModelIndex(), index.row(), index.row())
        del self.notes[index.row()]
        self.endRemoveRows()
        return True


class NoteApp(QWidget):
    def __init__(self):
        super().__init__()

        self.model = NoteModel()
        self.view = QListView()
        self.view.setModel(self.model)
        self.view.clicked.connect(self.remove_note)

        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Enter your note here...")
        self.add_button = QPushButton("Add Note")
        self.add_button.clicked.connect(self.add_note)

        layout = QVBoxLayout()
        layout.addWidget(self.note_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.view)

        self.setLayout(layout)

    def add_note(self):
        note = self.note_input.text()
        if self.model.add_note(note):
            self.note_input.clear()
        else:
            QMessageBox.warning(
                self,
                "Invalid Note",
                "Note cannot be empty or consist of only whitespace",
            )

    def remove_note(self, index):
        self.model.remove_note(index)
