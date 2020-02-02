# --*-- encode: utf-8 --*--

from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core
from vars import company_name, delete_icon, update_icon, number_pattern, name_patter
from database import Bill, BillDB
from functools import partial
import xlsxwriter as xl
import datetime
import sys

###############################################################
### BILLING PANEL                                           ###
###############################################################

def saveFileDialog():
    options = qt.QFileDialog.Options()
    options |= qt.QFileDialog.DontUseNativeDialog
    file_name, _ = qt.QFileDialog.getSaveFileName(tab_win, \
        "QFileDialog.getSaveFileName()","","MS Excel Files (*.xlsx);;All Files (*)", \
            options=options)
    return file_name

### -------------------------------------------------------------- ###

def del_bill_item(listing_id):
    my_bill.del_item(listing_id)
    update_current_bill()

### -------------------------------------------------------------- ###

def add_bill_item():
    item_name = cbm_add_item.currentText()
    item_cost = my_bill_db.get_item_by_name(item_name)[0][2]
    quantity = inp_itm_quantity.text()

    if not number_pattern.fullmatch(quantity):
        display_error("Invalid Quantity !!!")
    else:
        my_bill.add_item(item_name, item_cost, quantity)
        update_current_bill()
        inp_itm_quantity.setText("")

### -------------------------------------------------------------- ###

def new_bill():
    my_bill.reset_db()
    update_current_bill()

### -------------------------------------------------------------- ###

def save_bill_in_xlsx():
    bill_items = my_bill.get_items()
    bill_items_number = len(bill_items) if bill_items is not None else 0
    if bill_items_number > 0:
        file_name = saveFileDialog()

        if file_name:
            # Add extension if extension not added by default
            if not file_name[-5:].lower() == ".xlsx":
                file_name += ".xlsx"
            
            with xl.Workbook(file_name) as wb:
                # Create a worksheet
                ws = wb.add_worksheet()

                # Predefine formats 
                company_name_format = wb.add_format({'bold': True, 'font_color': 'red', 'font_size' : 18, 'border' : 1, 'align' : 'center', 'bg_color' : 'yellow'})
                total_bill_format = wb.add_format({'bold': True, 'font_color': 'blue', 'border' : 1})
                head_format = wb.add_format({'bold' : True, 'border' : 1, 'bg_color' : '#707070'})
                data_format = wb.add_format({'border' : 1})

                ws.set_column(0, 0, 30)
                ws.set_column(1, 3, 15)

                # Merge First row columns for header
                ws.merge_range(0, 0, 0, 3, company_name, company_name_format)
                ws.write(1, 0, "Name", head_format)
                ws.write(1, 1, "Unit Price", head_format)
                ws.write(1, 2, "Quantity", head_format)
                ws.write(1, 3, "Total Price", head_format)

                total_bill_cost = 0
                for row, bill_item in enumerate(bill_items, start = 2):
                    _, item_name, unit_cost, quantity = bill_item
                    total_cost = unit_cost * quantity
                    total_bill_cost += total_cost
                    ws.write(row, 0, item_name, data_format)
                    ws.write(row, 1, unit_cost, data_format)
                    ws.write(row, 2, quantity, data_format)
                    ws.write(row, 3, total_cost, data_format)
                
                # Show Total in Bill
                curent_time = datetime.datetime.now().strftime("%d %b %Y %I:%M %p")
                ws.merge_range(bill_items_number + 2, 0, bill_items_number + 2, 1, "Date: " + curent_time, data_format)
                ws.write(bill_items_number + 2, 2, "Total Bill", total_bill_format)
                ws.write(bill_items_number + 2, 3, total_bill_cost, total_bill_format)

### -------------------------------------------------------------- ###

def update_combo_box_list():
    # Get List from Database
    item_list = my_bill_db.get_items()

    # Clear Item List
    cbm_add_item.clear()

    for item in item_list:
        _, item_name, _ = item

        # Add Item in List
        cbm_add_item.addItem(item_name)
    
    # Refresh Combo Box
    cbm_add_item.update()

### -------------------------------------------------------------- ###

def update_current_bill():
    # Fetch all items from Bill
    bill_items = my_bill.get_items()
    bill_items_number = len(bill_items) if bill_items is not None else 0

    # Clean Table if already exist
    while tbl_current_bill.rowCount() > 0:
        tbl_current_bill.removeRow(0)

    # Create table for Bill Items
    tbl_current_bill.setRowCount(bill_items_number + 1 if bill_items_number > 0 else 0)
    tbl_current_bill.setColumnCount(5)
    tbl_current_bill.verticalHeader().setVisible(False)
    tbl_current_bill.setHorizontalHeaderLabels(("Name", "Unit Cost", "Quantity", "Total Cost", "Delete"))

    total_bill_amount = 0
    
    if bill_items is not None:
        for row, bill_item in enumerate(bill_items):
            # Extract Bill Items
            listing_id, itm_name, unit_cost, quantity = bill_item

            # Calculate Item Cost
            total_cost = float(unit_cost) * int(quantity)

            # Calculate Total Bill Amount
            total_bill_amount += total_cost

            # Add list in table
            tbl_current_bill.setItem(row, 0, qt.QTableWidgetItem(itm_name))
            tbl_current_bill.setItem(row, 1, qt.QTableWidgetItem(str(unit_cost)))
            tbl_current_bill.setItem(row, 2, qt.QTableWidgetItem(str(quantity)))
            tbl_current_bill.setItem(row, 3, qt.QTableWidgetItem(str(total_cost)))

            # Button to delete item from Bill
            btl_del_item_from_bill = qt.QPushButton()
            btl_del_item_from_bill.setIcon(gui.QIcon(delete_icon))
            btl_del_item_from_bill.setFlat(True)
            btl_del_item_from_bill.clicked.connect(partial(del_bill_item, listing_id))
            tbl_current_bill.setCellWidget(row, 4, btl_del_item_from_bill)
        
        # Display Final Total
        tbl_current_bill.setSpan(bill_items_number, 0, 1, 3)
        tbl_current_bill.setSpan(bill_items_number, 3, 1, 2)
        tbl_current_bill.setItem(bill_items_number, 0, qt.QTableWidgetItem("Total Bill: "))
        tbl_current_bill.setItem(bill_items_number, 3, qt.QTableWidgetItem(str(total_bill_amount)))
        tbl_current_bill.setItem(bill_items_number, 4, qt.QTableWidgetItem(""))
    
    # Update the Widget
    tbl_current_bill.update()

### -------------------------------------------------------------- ###

def bill_window():
    # Create main Window
    bill_win = qt.QWidget()

    # Create Vertical / Columnar Layout
    vbox = qt.QVBoxLayout()

    # Create Horizontal / row layout for items in same line
    hbox_row1 = qt.QHBoxLayout()
    hbox_row3 = qt.QHBoxLayout()

    # Create Widgets for first row
    global cbm_add_item
    cbm_add_item = qt.QComboBox()
    update_combo_box_list()
    
    global inp_itm_quantity
    inp_itm_quantity = qt.QLineEdit()

    # Button for adding item to bill
    btn_add_item_to_bill = qt.QPushButton("Add to Bill")
    btn_add_item_to_bill.clicked.connect(add_bill_item)

    # Add Widgets to Horizontal Box row 1
    hbox_row1.addWidget(cbm_add_item)
    hbox_row1.addWidget(inp_itm_quantity)
    hbox_row1.addWidget(btn_add_item_to_bill)
    hbox_row1.addStretch()

    # Create Widgets for 2nds row i.e. central part
    global tbl_current_bill
    tbl_current_bill = qt.QTableWidget()
    update_current_bill()

    # Create Button for Row 3
    btn_save = qt.QPushButton("Save Bill")
    btn_new_bill = qt.QPushButton("New Bill")

    # Actions for buttons
    btn_save.clicked.connect(save_bill_in_xlsx)
    btn_new_bill.clicked.connect(new_bill)

    hbox_row3.addWidget(btn_save)
    hbox_row3.addStretch()
    hbox_row3.addWidget(btn_new_bill)

    # Add Rows to main Window
    vbox.addLayout(hbox_row1)
    vbox.addWidget(tbl_current_bill)
    vbox.addLayout(hbox_row3)

    # Display the Window
    bill_win.setLayout(vbox)

    # Return Billing widget
    return bill_win

###############################################################
### ADMIN PANEL                                             ###
###############################################################

def display_error(display_message):
    msg_box = qt.QMessageBox()
    msg_box.setIcon(qt.QMessageBox.Critical)
    msg_box.setText(display_message)
    msg_box.setWindowTitle("Error")
    msg_box.exec_()

### -------------------------------------------------------------- ###

def update_itm_cost(itm_id, itm_cost_widget):
    itm_cost = itm_cost_widget.text()

    # Check whether pattern match
    if not number_pattern.fullmatch(itm_cost):
        display_error("Incorrect Amount !!!")
    elif not number_pattern.fullmatch(str(itm_id)):
        display_error("System Error !!!")
    else:
        my_bill_db.update_cost(itm_id, itm_cost)
        update_table_items()

### -------------------------------------------------------------- ###

def delete_itm(itm_id):
    my_bill_db.del_item(itm_id)
    update_table_items()

### -------------------------------------------------------------- ###

def add_item(itm_name_widget, itm_cost_widget):
    itm_name = itm_name_widget.text()
    itm_cost = itm_cost_widget.text()
    if not number_pattern.fullmatch(itm_cost):
        display_error("Incorrect Amount !!!")
    elif not name_patter.fullmatch(itm_name):
        display_error("Incorrect Name !!!")
    else:
        my_bill_db.add_item(itm_name, itm_cost)
        update_table_items()
        update_combo_box_list()
        itm_name_widget.setText("")
        itm_cost_widget.setText("")

### -------------------------------------------------------------- ###

def update_table_items():

    # Get Items from Bill Database
    items = my_bill_db.get_items()

    # Set Row and Columns for Bill Database
    tbl_items.setRowCount(len(items) if items is not None else 0)
    tbl_items.setColumnCount(5)
    tbl_items.setHorizontalHeaderLabels(("Delete Item", "Name", "Unit Cost", "New Cost", "Update Cost"))
    tbl_items.verticalHeader().setVisible(False)
    if items is not None:
        for row, item in enumerate(items):
            itm_id, itm_name, itm_cost = item

            # Create Button for delete
            btn_del_itm = qt.QPushButton()
            btn_del_itm.setIcon(gui.QIcon(delete_icon))
            btn_del_itm.setIconSize(core.QSize(24,24))
            btn_del_itm.setFlat(True)
            btn_del_itm.clicked.connect(partial(delete_itm, itm_id))
            tbl_items.setCellWidget(row, 0, btn_del_itm)

            tbl_items.setItem(row, 1, qt.QTableWidgetItem(itm_name))
            tbl_items.setItem(row, 2, qt.QTableWidgetItem(str(itm_cost)))

            inp_new_cost = qt.QLineEdit()
            btn_udpate_cost = qt.QPushButton("")
            btn_udpate_cost.setIcon(gui.QIcon(update_icon))
            btn_udpate_cost.setFlat(True)
            btn_udpate_cost.clicked.connect(partial(update_itm_cost, itm_id, inp_new_cost))

            tbl_items.setCellWidget(row, 3, inp_new_cost)
            tbl_items.setCellWidget(row, 4, btn_udpate_cost)

    # refresh Widget
    tbl_items.update()

### -------------------------------------------------------------- ###

def admin_window():
    # Create main Window
    admin_win = qt.QWidget()

    # Create Vertical Layout for Admin Tab
    vbox = qt.QVBoxLayout()

    # Create Horizontal Layout for admin row 1
    hbox_row1 = qt.QHBoxLayout()

    # Create widgets for row 1
    lbl_itm_name = qt.QLabel("Item Name: ")
    inp_itm_name = qt.QLineEdit()
    lbl_itm_spaces = qt.QLabel("     ")
    lbl_itm_cost = qt.QLabel("Item Cost: ")
    inp_itm_cost = qt.QLineEdit()
    btn_add_itm = qt.QPushButton("Add Item")

    # Action for Button
    btn_add_itm.pressed.connect(partial(add_item, inp_itm_name, inp_itm_cost))

    # Add Widgets to row 1
    hbox_row1.addWidget(lbl_itm_name)
    hbox_row1.addWidget(inp_itm_name)
    hbox_row1.addWidget(lbl_itm_spaces)
    hbox_row1.addWidget(lbl_itm_cost)
    hbox_row1.addWidget(inp_itm_cost)
    hbox_row1.addStretch()
    hbox_row1.addWidget(btn_add_itm)

    global tbl_items
    # Create Table widget to Show Items
    tbl_items = qt.QTableWidget()
    update_table_items()

    # Add Hbox on 1st Row
    vbox.addLayout(hbox_row1)
    vbox.addWidget(tbl_items)

    # Set Admin Widget Layout to Vbox
    admin_win.setLayout(vbox)

    # Return Admin Widget
    return admin_win

###############################################################
### MAIN EXECUTION                                          ###
###############################################################

if __name__ == "__main__":

    # Create objects of database classes
    my_bill = Bill()
    my_bill_db = BillDB()
    my_bill_db.create_table()
    #my_bill.reset_db()

    # Create a system app   
    app = qt.QApplication(sys.argv)

    # Create a tabbed window
    tab_win = qt.QTabWidget()
    tab_win.setWindowTitle(company_name)

    # set Getmetry of tabbed window
    tab_win.setGeometry(100, 100, 800, 600)

    # Add Main and Admin tabs to tab widget
    tab_win.addTab(bill_window(), "Billing")
    tab_win.addTab(admin_window(), "Update Inventory")

    tab_win.show()

    # Close the app on system exit
    sys.exit(app.exec_())