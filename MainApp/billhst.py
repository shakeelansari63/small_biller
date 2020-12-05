from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core
from .db import BillHist
from .setting import setting
from functools import partial
from .bill import BillWin


class BillHistWin(qt.QWidget):
    def __init__(self):
        # Initialize parent
        super().__init__()

        # Build Database Object for Bill
        self.bill = BillHist()

        # Build Window
        self.build_ui()

    def build_ui(self):
        # main layout
        self.main = qt.QVBoxLayout()

        # Search Row
        srch_row = qt.QHBoxLayout()
        self.search_bill = qt.QLineEdit()
        self.search_bill.setPlaceholderText('Search Bill')
        self.search_bill.textChanged.connect(self.refresh_table)
        srch_row.addWidget(self.search_bill)
        srch_row.addStretch()

        # View Table
        self.billtbl = qt.QTableWidget()
        # Remove edit triggers
        self.billtbl.setEditTriggers(qt.QTableWidget.NoEditTriggers)
        # Remove Grid Lines
        self.billtbl.setShowGrid(False)
        # Remove Headers
        self.billtbl.verticalHeader().setVisible(False)
        self.billtbl.horizontalHeader().setVisible(False)
        # Remove Focus/Selection Policy
        self.billtbl.setFocusPolicy(core.Qt.NoFocus)
        self.billtbl.setSelectionMode(qt.QTableWidget.NoSelection)
        # Resize horizontal and vertical length
        hheader = self.billtbl.horizontalHeader()
        vheader = self.billtbl.verticalHeader()
        hheader.setSectionResizeMode(qt.QHeaderView.ResizeToContents)
        hheader.setResizeContentsPrecision(20)
        vheader.setSectionResizeMode(qt.QHeaderView.Fixed)
        vheader.setDefaultSectionSize(32)
        # Refresh Bills Tables
        self.refresh_table()

        # Refresh Row
        ref_row = qt.QHBoxLayout()
        self.refresh = qt.QPushButton('Refresh')
        self.new_bill = qt.QPushButton('New Bill')
        self.refresh.clicked.connect(self.refresh_table)
        self.new_bill.clicked.connect(self.create_new_bill)
        ref_row.addWidget(self.refresh)
        ref_row.addStretch()
        ref_row.addWidget(self.new_bill)

        self.main.addLayout(srch_row)
        self.main.addWidget(self.billtbl)
        self.main.addLayout(ref_row)

        # Set main Layout
        self.setLayout(self.main)

    def update_table(self, bills):
        # Set row and columns
        self.billtbl.setRowCount(
            len(bills) + 1 if bills else 1
        )
        self.billtbl.setColumnCount(10)

        # Headers
        bold_font = gui.QFont()
        bold_font.setBold(True)

        billid = qt.QLabel('Bill Id   ')
        billid.setFont(bold_font)
        cusname = qt.QLabel('Customer Name   ')
        cusname.setFont(bold_font)
        cusphone = qt.QLabel('Customer Phone   ')
        cusphone.setFont(bold_font)
        devaddr = qt.QLabel('Delivery Address   ')
        devaddr.setFont(bold_font)
        billamt = qt.QLabel('Total Bill Ammount   ')
        billamt.setFont(bold_font)
        deldate = qt.QLabel('Delivery Date   ')
        deldate.setFont(bold_font)
        upddate = qt.QLabel('Update Date   ')
        upddate.setFont(bold_font)

        # Add Headers
        self.billtbl.setCellWidget(
            0, 1, billid
        )
        self.billtbl.setCellWidget(
            0, 2, cusname
        )
        self.billtbl.setCellWidget(
            0, 3, cusphone
        )
        self.billtbl.setCellWidget(
            0, 4, devaddr
        )
        self.billtbl.setCellWidget(
            0, 5, billamt
        )
        self.billtbl.setCellWidget(
            0, 6, deldate
        )
        self.billtbl.setCellWidget(
            0, 7, upddate
        )

        # Add Row Data
        if bills:
            for r_num, (bill_id, cust_name, cust_phone, del_addr, bill_amt, del_date, upd_date) in enumerate(bills, start=1):
                del_itm = qt.QPushButton('  ')
                del_itm.setIcon(gui.QIcon(setting['delbtn']))
                del_itm.setFlat(True)
                del_itm.clicked.connect(partial(self.delete_bill, bill_id))
                self.billtbl.setCellWidget(
                    r_num, 0, del_itm
                )

                self.billtbl.setCellWidget(
                    r_num, 1, qt.QLabel(str(bill_id) + '   ')
                )

                self.billtbl.setCellWidget(
                    r_num, 2, qt.QLabel(str(cust_name) + '   ')
                )

                self.billtbl.setCellWidget(
                    r_num, 3, qt.QLabel(str(cust_phone) + '   ')
                )

                self.billtbl.setCellWidget(
                    r_num, 4, qt.QLabel(str(del_addr) + '   ')
                )

                self.billtbl.setCellWidget(
                    r_num, 5, qt.QLabel(str(bill_amt) + '   ')
                )

                self.billtbl.setCellWidget(
                    r_num, 6, qt.QLabel(str(del_date) + '   ')
                )

                self.billtbl.setCellWidget(
                    r_num, 7, qt.QLabel(str(upd_date) + '   ')
                )

                # Buttons
                bill_dtl = qt.QPushButton('Bill Detail')
                bill_dtl.clicked.connect(partial(self.see_bill, bill_id))
                export_bill = qt.QPushButton('Export in Excel')
                export_bill.clicked.connect(partial(self.export_xls, bill_id))

                self.billtbl.setCellWidget(
                    r_num, 8, bill_dtl
                )

                self.billtbl.setCellWidget(
                    r_num, 7, export_bill
                )

    def refresh_table(self):
        search_text = self.search_bill.text()
        if search_text == '' or search_text is None:
            search_text = ''

        # Get Bills
        bills = self.bill.search_bill(search_text)

        # Update table with bills
        self.update_table(bills)

    def delete_bill(self, bill_id):
        self.bill.delete_bill(bill_id)

        self.refresh_table()

    def see_bill(self, bill_id):
        bill = BillWin()
        bill.open(bill_id)

    def export_xls(self, bill_id):
        pass

    def create_new_bill(self):
        bill = BillWin()
        bill.open()
