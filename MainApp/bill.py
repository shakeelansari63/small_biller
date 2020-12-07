from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core
from .db import Bill, Inventory, BillHist
from .setting import setting
from .alert import MsgCloseConfirm, MsgErrBox, MsgSucBox
from datetime import date
from functools import partial
import json


class BillWin(qt.QDialog):
    def __init__(self, bill_id=None):
        # Initialize parent
        super().__init__()

        # Build Database Object for Bill
        self.bill = Bill()
        self.inv = Inventory()
        self.billhst = BillHist()

        # Variable to detect if case is saved
        self.saved = False

        # Cleanup Bill database for initialization
        self.bill.reset_db()

        # Set Bill Id is available
        self.bill_id = bill_id

        # Build Window
        self.build_ui()

    def build_ui(self):
        # Define Validators
        self.define_validators()

        # Create main layout
        self.main = qt.QFormLayout()

        # Form Items
        self.cust_name = qt.QLineEdit()
        self.cust_name.setPlaceholderText('Customer Name')
        self.cust_name.setValidator(self.name_vald)

        self.cust_phone = qt.QLineEdit()
        self.cust_phone.setPlaceholderText('Customer Phone')
        self.cust_phone.setValidator(self.phone_vald)

        self.delv_addr = qt.QTextEdit()
        self.delv_addr.setPlaceholderText('Delivery Address')

        self.delv_date = qt.QDateEdit()
        self.delv_date.setDate(date.today())

        self.cgst = qt.QLineEdit()
        self.cgst.setPlaceholderText('C-GST')
        self.cgst.setValidator(self.real_vald)
        self.cgst.setText(setting['cgst'])

        self.sgst = qt.QLineEdit()
        self.sgst.setPlaceholderText('S-GST')
        self.sgst.setValidator(self.real_vald)
        self.sgst.setText(setting['sgst'])

        self.itm_name = qt.QComboBox()
        self.itm_name.setPlaceholderText('Select Item')
        self.itm_name.setValidator(self.name_vald)
        self.populate_bill_item_names()

        self.itm_qty = qt.QLineEdit()
        self.itm_qty.setPlaceholderText('Quantity')
        self.itm_qty.setValidator(self.int_999_vald)

        self.no_days = qt.QLineEdit()
        self.no_days.setPlaceholderText('Number of Days')
        self.no_days.setValidator(self.int_99_vald)

        self.add_to_bill = qt.QPushButton('Add to Bill')
        self.add_to_bill.clicked.connect(self.add_item_bill)

        self.bill_table = qt.QTableWidget()
        # Remove edit triggers
        self.bill_table.setEditTriggers(qt.QTableWidget.NoEditTriggers)
        # Remove Grid Lines
        self.bill_table.setShowGrid(False)
        # Remove Headers
        self.bill_table.verticalHeader().setVisible(False)
        self.bill_table.horizontalHeader().setVisible(False)
        # Remove Focus/Selection Policy
        self.bill_table.setFocusPolicy(core.Qt.NoFocus)
        self.bill_table.setSelectionMode(qt.QTableWidget.NoSelection)
        # Resize horizontal and vertical length
        hheader = self.bill_table.horizontalHeader()
        vheader = self.bill_table.verticalHeader()
        hheader.setSectionResizeMode(qt.QHeaderView.ResizeToContents)
        hheader.setResizeContentsPrecision(20)
        vheader.setSectionResizeMode(qt.QHeaderView.Fixed)
        vheader.setDefaultSectionSize(36)

        self.submit_bill = qt.QPushButton('Save Bill')
        self.submit_bill.clicked.connect(self.save_bill)

        self.total_bill_amt = qt.QLineEdit()
        self.total_bill_amt.setReadOnly(True)
        self.total_bill_amt.setFocusPolicy(core.Qt.NoFocus)
        self.total_bill_amt.setText('0')

        self.final_bill_amt_with_gst = qt.QLineEdit()
        self.final_bill_amt_with_gst.setReadOnly(True)
        self.final_bill_amt_with_gst.setFocusPolicy(core.Qt.NoFocus)
        self.final_bill_amt_with_gst.setText('0')

        # Populate Fields if editing existing bill
        if self.bill_id:
            self.populate_bill_fields()

        # Update Table
        self.cgst.textChanged.connect(self.update_bill_table)
        self.sgst.textChanged.connect(self.update_bill_table)
        self.update_bill_table()

        # Building Form
        # Customer Name
        self.main.addRow(
            qt.QLabel('Customer Name:   '),
            self.cust_name
        )

        # Customer Phone
        self.main.addRow(
            qt.QLabel('Customer Phone:   '),
            self.cust_phone
        )

        # Delivery Address
        self.main.addRow(
            qt.QLabel('Delivery Address:   '),
            self.delv_addr
        )

        # Delivery Date
        self.main.addRow(
            qt.QLabel('Delivery Date:   '),
            self.delv_date
        )

        # Add Items to bill
        item_col = qt.QVBoxLayout()
        item_row = qt.QHBoxLayout()
        item_row.addWidget(self.itm_name)
        item_row.addWidget(self.itm_qty)
        item_row.addWidget(self.no_days)
        item_row.addWidget(self.add_to_bill)
        item_row.addStretch()
        item_col.addLayout(item_row)
        item_col.addWidget(self.bill_table)
        self.main.addRow(
            qt.QLabel('Bill Items:   '),
            item_col
        )

        # Bill Total
        self.main.addRow(
            qt.QLabel('Total Amount:   '),
            self.total_bill_amt
        )

        # CGST
        self.main.addRow(
            qt.QLabel('C-GST:   '),
            self.cgst
        )

        # SGST
        self.main.addRow(
            qt.QLabel('S-GST:   '),
            self.sgst
        )

        # Bill Total
        self.main.addRow(
            qt.QLabel('Total Amount With GST:   '),
            self.final_bill_amt_with_gst
        )

        # Submit Row
        subrow = qt.QHBoxLayout()
        subrow.addStretch()
        subrow.addWidget(self.submit_bill)
        self.main.addRow(
            qt.QLabel(''),
            subrow
        )

        # Set Layout
        self.setLayout(self.main)

    def open(self):

        # Set Window Title and Icon
        self.setWindowIcon(gui.QIcon(setting['appicon']))
        self.setWindowTitle('New Bill')

        # Show Window
        self.showMaximized()
        self.setModal(True)
        self.exec()

    def save_bill(self):
        # Get all data fields
        cust_name = self.cust_name.text()
        cust_phone = self.cust_phone.text()
        delv_addr = self.delv_addr.toPlainText().replace("'", "''")
        delv_date = self.delv_date.date().toPyDate()
        cgst = float(self.cgst.text()) if self.cgst.text() != '' else 0
        sgst = float(self.sgst.text()) if self.sgst.text() != '' else 0
        total_bill_amt = float(self.total_bill_amt.text()
                               ) if self.total_bill_amt.text() != '' else 0
        final_bill_amt_with_gst = float(self.final_bill_amt_with_gst.text()
                                        ) if self.final_bill_amt_with_gst.text() != 0 else 0
        bill_items = json.dumps(self.bill.get_items())

        # Save to bills History database
        if cust_name != '' and cust_phone != '' and delv_addr != '' and total_bill_amt != 0:
            if self.bill_id:
                # Update Bill
                self.billhst.update_bill(self.bill_id, cust_name, cust_phone, delv_addr,
                                         bill_items, cgst, sgst, total_bill_amt,
                                         final_bill_amt_with_gst, delv_date)
            else:
                # Save Bill
                new_bill_id = self.billhst.save_bill(cust_name, cust_phone, delv_addr,
                                                     bill_items, cgst, sgst, total_bill_amt,
                                                     final_bill_amt_with_gst, delv_date)

            # Save and Close
            if (self.bill_id is not None) or (new_bill_id is not None):
                self.saved = True
                self.close()
                MsgSucBox('Bill Saved Successfully')
            else:
                MsgErrBox('Unable to save data')

        else:
            MsgErrBox('Missing Data')

    def closeEvent(self, event):
        if self.saved:
            event.accept()
        else:
            MsgCloseConfirm(self.save_bill, event.accept, event.ignore)

    def define_validators(self):
        name_re = core.QRegExp(r'[A-Za-z]+[\s]{0,1}[A-Za-z]*')
        self.name_vald = gui.QRegExpValidator(name_re)

        phone_re = core.QRegExp(r'[\+]{0,1}[0-9]{12}')
        self.phone_vald = gui.QRegExpValidator(phone_re)

        real_re = core.QRegExp(r'[0-9]+[\.]{0,1}[0-9]*')
        self.real_vald = gui.QRegExpValidator(real_re)

        self.int_99_vald = gui.QIntValidator(1, 99)

        self.int_999_vald = gui.QIntValidator(1, 999)

    def add_item_bill(self):
        # Get Input and add item to bill
        idx = self.itm_name.currentIndex()

        _, itm_name, itm_unit_cost = self.inv_items[idx]

        if self.itm_qty.text() != '' and self.no_days.text() != '':
            itm_qty = int(self.itm_qty.text())
            no_days = int(self.no_days.text())

            # Add to bill
            self.bill.add_item(itm_name, itm_unit_cost, itm_qty, no_days)

        # reset the Item Fields
        self.itm_qty.setText('')
        self.no_days.setText('')

        # Update Table
        self.update_bill_table()

    def delete_item_from_bill(self, lst_id):
        # Delete item
        self.bill.del_item(lst_id)

        # Update table
        self.update_bill_table()

    def update_bill_table(self):

        # Get all Bill Items
        bill_itms = self.bill.get_items()

        # Set table rows and columns
        self.bill_table.setColumnCount(6)
        self.bill_table.setRowCount(len(bill_itms) + 1 if bill_itms else 1)

        # Set Header for table
        bold_font = gui.QFont()
        bold_font.setBold(True)
        it_nm = qt.QLabel('Item Name   ')
        it_nm.setFont(bold_font)
        it_cs = qt.QLabel('Item Unit Cost   ')
        it_cs.setFont(bold_font)
        it_qt = qt.QLabel('Item Quantity   ')
        it_qt.setFont(bold_font)
        it_dy = qt.QLabel('Number of Days   ')
        it_dy.setFont(bold_font)
        tt_cs = qt.QLabel('Total Cost   ')
        tt_cs.setFont(bold_font)

        # Set header row
        self.bill_table.setCellWidget(0, 1, it_nm)
        self.bill_table.setCellWidget(0, 2, it_cs)
        self.bill_table.setCellWidget(0, 3, it_qt)
        self.bill_table.setCellWidget(0, 4, it_dy)
        self.bill_table.setCellWidget(0, 5, tt_cs)

        # Loop over bill items
        total_bill_amt = 0
        if bill_itms:
            for row_num, (lst_id, lst_nm, lst_cs, lst_qt, ls_dy) in enumerate(bill_itms, start=1):
                # Calculate itme's total cost
                itm_total_cost = lst_cs * lst_qt * ls_dy
                total_bill_amt += itm_total_cost

                # Delete item's button
                del_itm = qt.QPushButton('')
                del_itm.setIcon(gui.QIcon(setting['delbtn']))
                del_itm.setFlat(True)
                del_itm.clicked.connect(
                    partial(self.delete_item_from_bill, lst_id))

                # Display item in table
                self.bill_table.setCellWidget(
                    row_num, 0, del_itm
                )
                self.bill_table.setCellWidget(
                    row_num, 1, qt.QLabel(str(lst_nm))
                )
                self.bill_table.setCellWidget(
                    row_num, 2, qt.QLabel(str(lst_cs))
                )
                self.bill_table.setCellWidget(
                    row_num, 3, qt.QLabel(str(lst_qt))
                )
                self.bill_table.setCellWidget(
                    row_num, 4, qt.QLabel(str(ls_dy))
                )
                self.bill_table.setCellWidget(
                    row_num, 5, qt.QLabel(str(itm_total_cost))
                )

            # Refresh Table
            self.bill_table.update()

        # Set total Bill amount
        self.total_bill_amt.setText(str(total_bill_amt))

        # Calculate CGST
        cgst = float(self.cgst.text()) if self.cgst.text() != '' else 0
        sgst = float(self.sgst.text()) if self.sgst.text() != '' else 0

        cgst_value = (cgst / 100) * total_bill_amt
        sgst_value = (sgst / 100) * total_bill_amt

        final_bill_amt_with_gst = total_bill_amt + cgst_value + sgst_value

        # Final bill amount with GST
        self.final_bill_amt_with_gst.setText(str(final_bill_amt_with_gst))

    def populate_bill_item_names(self):
        # Get list of all items in Inventory
        self.inv_items = self.inv.get_all_items()

        list_of_item_names = [it[1] for it in self.inv_items]

        if list_of_item_names:
            self.itm_name.addItems(list_of_item_names)

    def populate_bill_fields(self):
        # Fetch Bill Data
        bill_data = self.billhst.get_bill_by_id(self.bill_id)

        if bill_data:
            # Unpack Data
            (_, cust_name, cust_phone, delv_addr, items,
             cgst, sgst, tot_bill, tot_bill_w_gst, delv_date, _) = bill_data[0]

            delv_date = core.QDate.fromString(delv_date, 'yyyy-MM-dd')

            # Set data fields
            self.cust_name.setText(str(cust_name))
            self.cust_phone.setText(str(cust_phone))
            self.delv_addr.setPlainText(str(delv_addr))
            self.cgst.setText(str(cgst))
            self.sgst.setText(str(sgst))
            self.total_bill_amt.setText(str(tot_bill))
            self.final_bill_amt_with_gst.setText(str(tot_bill_w_gst))
            self.delv_date.setDate(delv_date)

            # Update Bills database with items
            bill_items = json.loads(items)

            for _, itm_nm, itm_cost, itm_qty, no_days in bill_items:
                self.bill.add_item(itm_nm, itm_cost, itm_qty, no_days)
