from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from models.Note import Note


class NotesModel(QAbstractListModel):
    def __init__(self, notes=None):
        super().__init__()
        self.notes = notes or []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            note = self.notes[index.row()]
            return f"{note.date.toString(Qt.DateFormat.ISODate)}: {note.text}"

    def rowCount(self, index):
        return len(self.notes)

    def addNote(self, note: Note, parent=None):
        if not note.text or not note.text.strip():
            QMessageBox.warning(
                parent,
                "Invalid Note",
                "Note cannot be empty or consist of only whitespace",
            )
            return
        self.beginInsertRows(
            self.index(len(self.notes)), len(self.notes), len(self.notes)
        )
        self.notes.append(note)
        self.endInsertRows()

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self.notes[index.row()].text = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable


class NoteDialog(QDialog):
    def __init__(self, parent=None, note=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit note")

        layout = QVBoxLayout()
        self.textEdit = QLineEdit(note.text if note else "")
        self.saveButton = QPushButton("Save")

        layout.addWidget(self.textEdit)
        layout.addWidget(self.saveButton)
        self.setLayout(layout)

        self.saveButton.clicked.connect(self.accept)

    def getNote(self):
        return Note(self.textEdit.text(), QDate.currentDate())


class NotesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.notesModel = NotesModel()
        self.listView = QListView()
        self.listView.setModel(self.notesModel)

        layout = QVBoxLayout()
        layout.addWidget(self.listView)
        self.setLayout(layout)

        self.createContextMenu()

    def createContextMenu(self):
        self.listView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.listView.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, position):
        menu = QMenu()

        addAction = QAction("Add note", self)
        addAction.triggered.connect(self.addNote)
        menu.addAction(addAction)

        editAction = QAction("Edit note", self)
        editAction.triggered.connect(self.editNote)
        menu.addAction(editAction)

        menu.exec(self.listView.mapToGlobal(position))

    def addNote(self):
        dialog = NoteDialog(self)
        if dialog.exec():
            self.notesModel.addNote(dialog.getNote(), self)

    def editNote(self):
        index = self.listView.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Error", "Choose note to edit")
            return

        note = self.notesModel.notes[index.row()]
        dialog = NoteDialog(self, note)
        if dialog.exec():
            if not dialog.textEdit.text() or not dialog.textEdit.text().strip():
                QMessageBox.warning(
                    self,
                    "Invalid Note",
                    "Note cannot be empty or consist of only whitespace",
                )
                return
            self.notesModel.setData(
                index, dialog.textEdit.text(), Qt.ItemDataRole.EditRole
            )
