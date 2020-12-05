from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core
from .bill import BillWin
from .admin import AdminWin
from .setting import setting
from qtmodern import styles as mstyle
import sys


class App(qt.QTabWidget):
    def __init__(self):
        # Create Application
        self.app = qt.QApplication(sys.argv)

        # Initialize parent class
        super().__init__()

        # High DPI App
        self.app.setAttribute(core.Qt.AA_UseHighDpiPixmaps)

        # Set Modern Style of App
        mstyle.dark(self.app)

    def run(self):
        # Set Title
        self.setWindowTitle(setting['appname'])

        # Set App Icon
        self.setWindowIcon(gui.QIcon(setting['appicon']))

        # Apply Tables
        self.addTab(BillWin(), 'Billing')
        self.addTab(AdminWin(), 'Inventory')

        # Maximised Window
        self.showMaximized()

        # Show window
        self.show()
        sys.exit(self.app.exec_())
