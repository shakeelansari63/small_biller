from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core
from .db import Bill
from .setting import setting
from .alert import MsgCloseConfirm


class BillWin(qt.QDialog):
    def __init__(self):
        # Initialize parent
        super().__init__()

        # Build Database Object for Bill
        self.bill = Bill()

        # Variable to detect if case is saved
        self.saved = False

        # Build Window
        self.build_ui()

    def build_ui(self):
        pass

    def open(self, bill_id=None):

        # Set Window Title and Icon
        self.setWindowIcon(gui.QIcon(setting['appicon']))
        self.setWindowTitle('New Bill')

        # Show Window
        self.setModal(True)
        self.exec()

    def save_bill(self):
        # Action to save bill

        # Close
        self.saved = True
        self.close()

    def closeEvent(self, event):
        if self.saved:
            event.accept()
        else:
            MsgCloseConfirm(self.save_bill, event.accept, event.ignore)
