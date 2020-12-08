from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core
from .db import BillHist
from .setting import setting
from functools import partial
from .bill import BillWin
import json
from .alert import MsgErrBox
import xlsxwriter as xl


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
            for r_num, (bill_id, cust_name, cust_phone, del_addr, _, _, _, _, bill_w_gst,  del_date, upd_date) in enumerate(bills, start=1):
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
                    r_num, 5, qt.QLabel(str(bill_w_gst) + '   ')
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
        bill = BillWin(bill_id)
        bill.open()

    def export_xls(self, bill_id):
        # Get Bill data
        bill_data = self.bill.get_bill_by_id(bill_id)

        if bill_data:
            # Unpack Data
            (_, cust_name, cust_phone, delv_addr, items,
             cgst, sgst, tot_bill, tot_bill_w_gst, delv_date, _) = bill_data[0]

        bill_items = json.loads(items)

        if bill_items:
            # Open dialog to get file name
            xl_file = self.file_dialog()

            # Check if Excel file is not empty
            if xl_file:
                # Apend File extension if not provided
                if not xl_file.lower().endswith('.xlsx'):
                    xl_file = xl_file + '.xlsx'

                # Open file for editting
                with xl.Workbook(xl_file) as wb:
                    # Add Wroksheet
                    ws = wb.add_worksheet()

                    # Predefine formats
                    company_name_format = wb.add_format({'bold': True,
                                                         'font_color': 'red', 'font_size': 18,
                                                         'border': 1, 'align': 'center', 'bg_color': 'yellow'
                                                         })
                    total_bill_format = wb.add_format({'bold': True, 'font_color': 'blue',
                                                       'border': 1})
                    head_format = wb.add_format({'bold': True, 'border': 1,
                                                 'bg_color': '#A0A0A0'})
                    data_format = wb.add_format({'border': 1})

                    # Set Column Width
                    ws.set_column(0, 0, 30)  # 0-0 column width is 30
                    ws.set_column(1, 4, 15)  # 1-4 columns width is 15

                    # Company Name Header
                    ws.merge_range(0, 0, 0, 4,
                                   setting['appname'], company_name_format)

                    # Customer and order details
                    ws.merge_range(1, 0, 1, 2, "Customer Name", head_format)
                    ws.merge_range(1, 3, 1, 4, cust_name, data_format)

                    ws.merge_range(2, 0, 2, 2, "Customer Phone", head_format)
                    ws.merge_range(2, 3, 2, 4, cust_phone, data_format)

                    ws.merge_range(3, 0, 3, 2, "Delivery Address", head_format)
                    ws.merge_range(3, 3, 3, 4, delv_addr, data_format)

                    ws.merge_range(4, 0, 4, 2, "Delivery Date", head_format)
                    ws.merge_range(4, 3, 4, 4, delv_date, data_format)

                    # 1 Row gap
                    ws.merge_range(5, 0, 5, 4, "", data_format)

                    ws.write(6, 0, "Name", head_format)
                    ws.write(6, 1, "Unit Price", head_format)
                    ws.write(6, 2, "Quantity", head_format)
                    ws.write(6, 3, "Number of Days", head_format)
                    ws.write(6, 4, "Total Price", head_format)

                    # Counter for further rows
                    cnt = 7

                    for rnum, (_, itm_name, itm_cost, itm_qty, no_days) in enumerate(bill_items):
                        # Calculate total Price
                        tot_price = float(itm_cost) * \
                            float(itm_qty) * float(no_days)
                        # Write data in sheet
                        ws.write(rnum + 7, 0, itm_name, data_format)
                        ws.write(rnum + 7, 1, itm_cost, data_format)
                        ws.write(rnum + 7, 2, itm_qty, data_format)
                        ws.write(rnum + 7, 3, no_days, data_format)
                        ws.write(rnum + 7, 4, str(tot_price), data_format)

                        # Increment COunter
                        cnt += 1
                    # 1 Row gap
                    ws.merge_range(cnt, 0, cnt, 4, "", data_format)

                    # Other Bill Details
                    ws.merge_range(cnt + 1, 0, cnt + 1, 2,
                                   "Bill Amount", head_format)
                    ws.merge_range(cnt + 1, 3, cnt + 1, 4,
                                   tot_bill, data_format)

                    ws.merge_range(cnt + 2, 0, cnt + 2, 2, "SGST", head_format)
                    ws.merge_range(cnt + 2, 3, cnt + 2, 4, sgst, data_format)

                    ws.merge_range(cnt + 3, 0, cnt + 3, 2, "CGST", head_format)
                    ws.merge_range(cnt + 3, 3, cnt + 3, 4, cgst, data_format)

                    ws.merge_range(cnt + 4, 0, cnt + 4, 2, "Total Bill With GST",
                                   head_format)
                    ws.merge_range(cnt + 4, 3, cnt + 4, 4, tot_bill_w_gst,
                                   total_bill_format)

        else:
            MsgErrBox('Bill is Empty')

    def create_new_bill(self):
        bill = BillWin()
        bill.open()

    def file_dialog(self):
        options = qt.QFileDialog.Options()
        options |= qt.QFileDialog.DontUseNativeDialog
        file_name, _ = qt.QFileDialog.getSaveFileName(self, "Save as Excel Sheet",
                                                      "", "MS Excel Files (*.xlsx);;All Files (*)",
                                                      options=options)
        return file_name
