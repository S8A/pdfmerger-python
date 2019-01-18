from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QTableWidget


import sys


class PDFMergerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['File', 'Start', 'End'])

        self.setCentralWidget(self.table)

        self.add_action = QAction('Add', self)
        #self.add_action.triggered.connect(self.addFile)

        self.clear_action = QAction('Clear', self)
        #self.clear_action.triggered.connect(self.removeAll)

        self.duplicate_action = QAction('Duplicate', self)
        #self.duplicate_action.triggered.connect(self.duplicate)

        self.remove_action = QAction('Remove', self)
        #self.remove_action.triggered.connect(self.remove)

        self.move_up_action = QAction('Move Up', self)
        #self.move_up_action.triggered.connect(self.move_up)

        self.move_down_action = QAction('Move Down', self)
        #self.move_down_action.triggered.connect(self.move_down)

        self.merge_action = QAction('Merge', self)
        #self.merge_action.triggered.connect(self.merge)

        toolbar = self.addToolBar('Main')
        toolbar.addAction(self.add_action)
        toolbar.addAction(self.clear_action)
        toolbar.addAction(self.duplicate_action)
        toolbar.addAction(self.remove_action)
        toolbar.addAction(self.move_up_action)
        toolbar.addAction(self.move_down_action)
        toolbar.addAction(self.merge_action)


class AppContext(ApplicationContext):           # 1. Subclass ApplicationContext
    def run(self):                              # 2. Implement run()
        window = PDFMergerWindow()
        version = self.build_settings['version']
        window.setWindowTitle("PDFMerger v" + version)
        window.resize(600, 400)
        window.show()
        return self.app.exec_()                 # 3. End run() with this line


if __name__ == '__main__':
    appctxt = AppContext()                      # 4. Instantiate the subclass
    exit_code = appctxt.run()                   # 5. Invoke run()
    sys.exit(exit_code)
