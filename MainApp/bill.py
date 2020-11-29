from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core
from .db import Bill, Inventory


class BillWin(qt.QWidget):
    def __init__(self):
        # Initialize parent
        super().__init__()

        # Build Database Object for Bill
        self.inv = Inventory()
        self.bill = Bill()

        # Build Window
        self.build_ui()

    def build_ui(self):
        pass
