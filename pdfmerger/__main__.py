from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import PyPDF2, sys
from .document import Document


class DocumentTableModel(QAbstractTableModel):
    """Internal model for the table of documents to merge."""

    def __init__(self, parent = None):
        super().__init__(parent)
        self.docs = []
        self.headers = ['File', 'Start', 'End']

    def rowCount(self, parent):
        """Returns the number of documents."""
        return len(self.docs)

    def columnCount(self, parent):
        """Returns the number of columns."""
        return len(self.headers)

    def flags(self, index):
        """Provides the properties (flags) of each column."""
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):
        """Provides the data for each cell."""
        row = index.row()
        col = index.column()

        if role == Qt.EditRole:
            if col == 1:
                return self.docs[row].start
            elif col == 2:
                return self.docs[row].end

        if role == Qt.DisplayRole:
            if col == 0:
                return self.docs[row].path
            elif col == 1:
                return self.docs[row].start
            elif col == 2:
                return self.docs[row].end

    def setData(self, index, value, role = Qt.EditRole):
        """Handles the modification of editable cells."""
        if role == Qt.EditRole:
            row = index.row()
            col = index.column()
            total_pages = self.docs[row].num_pages
            old_start = self.docs[row].start
            old_end = self.docs[row].end

            try:
                new_value = int(value)
                if col == 1 and new_value > 0 and new_value <= old_end:
                    self.docs[row].start = new_value
                    self.dataChanged.emit(index, index)
                    return True
                elif (col == 2 and new_value >= old_start
                        and new_value <= total_pages):
                    self.docs[row].end = new_value
                    self.dataChanged.emit(index, index)
                    return True
            except TypeError:
                return False
        return False

    def headerData(self, section, orientation, role):
        """Returns the appropriate header."""
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < len(self.headers):
                    return self.headers[section]

    def insertRows(self, row, count, parent = QModelIndex()):
        """Handles the insertion of document entries into the list."""
        self.beginInsertRows(parent, row, row + count - 1)
        for i in range(count):
            self.docs.insert(row, Document())
        self.endInsertRows()        
        return True

    def removeRows(self, row, count, parent = QModelIndex()):
        """Handles the removal of document entries from the list."""
        self.beginRemoveRows(parent, row, row + count - 1);
        for i in range(count):
            self.documents.pop(row)
        self.endRemoveRows()
        return True


class PDFMergerWindow(QMainWindow):
    """Main window of the PDF Merger application."""

    def __init__(self):
        super().__init__()
        self._create_ui()

    def _create_ui(self):
        """Creates the window's UI."""
        self.model = DocumentTableModel()

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.selection = self.table.selectionModel()
        self.selection.currentChanged.connect(self._toggle_buttons)

        self.setCentralWidget(self.table)

        self.add_action = QAction('Add')
        self.add_action.triggered.connect(self._add_file)

        self.clear_action = QAction('Clear')
        self.clear_action.triggered.connect(self._clear)

        self.duplicate_action = QAction('Duplicate')
        self.duplicate_action.triggered.connect(self._duplicate)

        self.remove_action = QAction('Remove')
        self.remove_action.triggered.connect(self._remove)

        self.move_up_action = QAction('Move Up')
        self.move_up_action.triggered.connect(self._move_up)

        self.move_down_action = QAction('Move Down')
        self.move_down_action.triggered.connect(self._move_down)

        self.merge_action = QAction('Merge')
        self.merge_action.triggered.connect(self._merge)

        toolbar = self.addToolBar('Main')
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.addAction(self.add_action)
        toolbar.addAction(self.clear_action)
        toolbar.addSeparator()
        toolbar.addAction(self.duplicate_action)
        toolbar.addAction(self.remove_action)
        toolbar.addSeparator()
        toolbar.addAction(self.move_up_action)
        toolbar.addAction(self.move_down_action)
        toolbar.addSeparator()
        toolbar.addAction(self.merge_action)

        self._toggle_buttons()

        self.setWindowTitle("PDFMerger")
        self.resize(600, 400)

    def _change_selection(self, index):
        """Changes the selected item to the one with the given index."""
        self.selection.setCurrentIndex(
            self.selection.currentIndex().siblingAtRow(index),
            QItemSelectionModel.SelectionFlag.ClearAndSelect)

    def _toggle_buttons(self):
        """Enables or disables buttons according to selected row."""
        current = self.selection.currentIndex().row()

        self.duplicate_action.setEnabled(False)
        self.remove_action.setEnabled(False)
        self.move_up_action.setEnabled(False)
        self.move_down_action.setEnabled(False)

        if current != -1:
            self.duplicate_action.setEnabled(True)
            self.remove_action.setEnabled(True)
            if current != 0:
                self.move_up_action.setEnabled(True)
            if current != len(self.model.docs) - 1:
                self.move_down_action.setEnabled(True)

        if len(self.model.docs) > 0:
            self.merge_action.setEnabled(True)
        else:
            self.merge_action.setEnabled(False)

    def _add_file(self):
        """Adds a PDF file to the end of the list."""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        to_open = file_dialog.getOpenFileNames(
            self, caption = 'Open file', filter = '*.pdf')

        for file in to_open[0]:
            doc = Document(file)
            self.model.layoutAboutToBeChanged.emit()
            self.model.docs.append(doc)
            self.model.layoutChanged.emit()

    def _remove(self):
        """Removes the current PDF entry from the list."""
        current = self.selection.currentIndex().row()
        self.model.layoutAboutToBeChanged.emit()
        self.model.docs.pop(current)
        self.model.layoutChanged.emit()
        if self.model.docs:
            self._change_selection(current - 1)
        else:
            self.selection.clear()

    def _clear(self):
        """Removes all entries from the PDF list."""
        self.model.layoutAboutToBeChanged.emit()
        self.model.docs.clear()
        self.model.layoutChanged.emit()
        self.selection.clear()

    def _duplicate(self):
        """Creates a copy of the current PDF entry."""
        current = self.selection.currentIndex().row()
        self.model.insertRows(current + 1, 1)
        self.model.docs[current + 1] = self.model.docs[current].copy()

    def _swap(self, i, j):
        """Swaps two PDF entries' positions in the list."""
        self.model.layoutAboutToBeChanged.emit()
        self.model.docs[i], self.model.docs[j] = (
            self.model.docs[j], self.model.docs[i])
        self.model.layoutChanged.emit()

    def _move_up(self):
        """Moves the current PDF entry up one position."""
        current = self.selection.currentIndex().row()
        self._swap(current - 1, current)
        self._change_selection(current - 1)

    def _move_down(self):
        """Moves the current PDF entry down one position."""
        current = self.selection.currentIndex().row()
        self._swap(current, current + 1)
        self._change_selection(current + 1)

    def _merge(self):
        """Merges the PDF entries in the list into one PDF and saves it."""
        if len(self.model.docs) > 0:
            merger = PyPDF2.PdfFileMerger()

            for doc in self.model.docs:
                pdf = PyPDF2.PdfFileReader(open(doc.path, 'rb'))
                page_range = (doc.start - 1, doc.end)
                merger.append(pdf, pages=page_range)

            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
            file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
            to_save = file_dialog.getSaveFileName(
                self, caption = 'Save file', filter = '*.pdf')

            if to_save[0]:
                with open(to_save[0], 'wb') as file:
                    merger.write(file)


def main():
    """Creates and shows the main window of the application."""
    app = QApplication(sys.argv)
    window = PDFMergerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
