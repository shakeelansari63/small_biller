from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core
from .db import Bill, Inventory, BillHist
from .setting import setting
from .alert import MsgSucBox


class AdminSetup(qt.QDialog):
    def __init__(self):
        # Initialize parent
        super().__init__()

        # Build Database Object for Bill
        self.inv = Inventory()
        self.bill = Bill()
        self.billhst = BillHist()

        # Build Window
        self.build_ui()

    def build_ui(self):
        # Build main layout
        main = qt.QVBoxLayout()

        # Reset Database
        resdb = qt.QPushButton('Reset Whole Database')
        resdb.clicked.connect(self.reset_db)
        # Reset Inventory
        resinv = qt.QPushButton('Reset Inventory')
        resinv.clicked.connect(self.reset_inv)
        # Reset Bill Database
        resbill = qt.QPushButton('Reset Bills')
        resbill.clicked.connect(self.reset_bill)

        main.addWidget(resdb)
        main.addWidget(resinv)
        main.addWidget(resbill)

        # Set layout for widget
        self.setLayout(main)

        # Set Window Option
        self.setWindowTitle('Admin Setup')
        self.setWindowIcon(gui.QIcon(setting['appicon']))

    def open(self):
        self.setModal(True)
        self.exec()

    def reset_db(self):
        self.inv.reset_db()
        self.bill.reset_db()
        self.billhst.reset_db()
        MsgSucBox('Database Reset Completed')

    def reset_inv(self):
        self.inv.reset_db()
        MsgSucBox('Inventory Reset Completed')

    def reset_bill(self):
        self.bill.reset_db()
        self.billhst.reset_db()
        MsgSucBox('Bills Reset Completed')
