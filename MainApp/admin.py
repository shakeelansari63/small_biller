from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core
from .db import Inventory
from .setup import AdminSetup
from functools import partial
from .alert import MsgErrBox, MsgSucBox


class AdminWin(qt.QWidget):
    def __init__(self):
        # Initialize parent
        super().__init__()

        # Create Inventory Object
        self.inv = Inventory()

        # Build Window
        self.build_ui()

    def build_ui(self):
        # Define Validators
        self.define_validators()

        # Main Layout
        self.main = qt.QVBoxLayout()

        # Add Item Row
        new_itm_row = qt.QHBoxLayout()

        # New Items
        self.new_item_name = qt.QLineEdit()
        self.new_item_name.setPlaceholderText('Item Name')
        self.new_item_name.setValidator(self.item_name_vald)

        self.new_item_cost = qt.QLineEdit()
        self.new_item_cost.setPlaceholderText('Item Cost')
        self.new_item_cost.setValidator(self.item_cost_vald)

        self.new_item_save = qt.QPushButton('Add to Inventory')
        self.new_item_save.clicked.connect(self.add_to_inventory)

        self.search_item = qt.QLineEdit()
        self.search_item.setPlaceholderText('Search Item')
        self.search_item.setValidator(self.item_name_vald)
        self.search_item.textChanged.connect(self.search_item_indb)

        new_itm_row.addWidget(qt.QLabel('Add New Item:  '))
        new_itm_row.addWidget(self.new_item_name)
        new_itm_row.addWidget(self.new_item_cost)
        new_itm_row.addWidget(self.new_item_save)
        new_itm_row.addStretch()
        new_itm_row.addWidget(self.search_item)

        # Table layout for Inventory Items
        self.invtab = qt.QTableWidget()
        # Remove edit triggers
        self.invtab.setEditTriggers(qt.QTableWidget.NoEditTriggers)
        # Remove Grid Lines
        self.invtab.setShowGrid(False)
        # Remove Headers
        self.invtab.verticalHeader().setVisible(False)
        self.invtab.horizontalHeader().setVisible(False)
        # Remove Focus/Selection Policy
        self.invtab.setFocusPolicy(core.Qt.NoFocus)
        self.invtab.setSelectionMode(qt.QTableWidget.NoSelection)
        # Update Table
        self.get_new_items()

        # Admin row
        admin_row = qt.QHBoxLayout()
        self.refresh_btn = qt.QPushButton('Refresh')
        self.refresh_btn.clicked.connect(self.refresh_table)
        self.admin = qt.QPushButton('Admin Setup')
        self.admin.clicked.connect(self.admin_window)
        # Add btn to row
        admin_row.addWidget(self.refresh_btn)
        admin_row.addStretch()
        admin_row.addWidget(self.admin)

        # Add Row to Main Layout
        self.main.addLayout(new_itm_row)
        self.main.addWidget(self.invtab)
        self.main.addLayout(admin_row)

        # Set layout of window
        self.setLayout(self.main)

    def define_validators(self):
        item_name_re = core.QRegExp(r'[A-Za-z\s]+')
        self.item_name_vald = gui.QRegExpValidator(item_name_re)

        item_cost_re = core.QRegExp(r'[0-9]+[\.]{0,1}[0-9]*')
        self.item_cost_vald = gui.QRegExpValidator(item_cost_re)

    def add_to_inventory(self):
        new_item_name = self.new_item_name.text()
        new_item_cost = self.new_item_cost.text()

        if new_item_name != '' and new_item_name is not None \
                and new_item_cost != '' and new_item_cost is not None:
            self.inv.add_item(new_item_name, new_item_cost)

            self.new_item_name.setText('')
            self.new_item_cost.setText('')

            self.get_new_items()

    def search_item_indb(self):
        # Search Text
        search_txt = self.search_item.text()

        # Build list of found items
        searched_items = self.inv.get_item_by_name_pattern(search_txt)

        # Update table
        self.build_item_list(searched_items)

    def get_new_items(self):
        new_items_list = self.inv.get_items()
        self.build_item_list(new_items_list)

    def build_item_list(self, item_list):

        # List table row and column
        self.invtab.setColumnCount(6)
        self.invtab.setRowCount(
            len(item_list) + 1 if item_list else 1
        )

        # Add Header row
        bold_font = gui.QFont()
        bold_font.setBold(True)
        itm_id = qt.QLabel('Item Id  ')
        itm_id.setFont(bold_font)
        itm_nm = qt.QLabel('Item Name  ')
        itm_nm.setFont(bold_font)
        itm_cs = qt.QLabel('Item Cost  ')
        itm_cs.setFont(bold_font)
        itm_upd_cs = qt.QLabel('Update Cost  ')
        itm_upd_cs.setFont(bold_font)
        itm_dl = qt.QLabel('Delete Item  ')
        itm_dl.setFont(bold_font)

        self.invtab.setCellWidget(0, 0, itm_id)
        self.invtab.setCellWidget(0, 1, itm_nm)
        self.invtab.setCellWidget(0, 2, itm_cs)
        self.invtab.setCellWidget(0, 3, itm_upd_cs)
        self.invtab.setSpan(0, 3, 1, 2)
        self.invtab.setCellWidget(0, 5, itm_dl)

        # Add items
        if item_list:
            for row_num, (item_id, item_name, item_cost) in enumerate(item_list, start=1):
                self.invtab.setCellWidget(
                    row_num, 0, qt.QLabel(str(item_id) + '  ')
                )

                self.invtab.setCellWidget(
                    row_num, 1, qt.QLabel(str(item_name) + '  ')
                )

                self.invtab.setCellWidget(
                    row_num, 2, qt.QLabel(str(item_cost) + '  ')
                )

                new_cost = qt.QLineEdit()
                new_cost.setPlaceholderText('New Cost')
                new_cost.setValidator(self.item_cost_vald)
                save_cost = qt.QPushButton('Save New Cost')
                save_cost.clicked.connect(partial(
                    self.save_new_cost, item_id, new_cost
                ))

                self.invtab.setCellWidget(
                    row_num, 3, new_cost
                )

                self.invtab.setCellWidget(
                    row_num, 4, save_cost
                )

                del_itm = qt.QPushButton('Delete')
                del_itm.clicked.connect(partial(self.del_item_fromdb, item_id))

                self.invtab.setCellWidget(
                    row_num, 5, del_itm
                )

        # Refresh Table
        self.invtab.update()

    def admin_window(self):
        adm = AdminSetup()
        adm.open()

    def save_new_cost(self, itm_id, new_cost_wig):
        # Get value of new cost
        new_cost = new_cost_wig.text()

        # Update cost if not empty
        if new_cost != '' and new_cost is not None:
            self.inv.update_cost(itm_id, new_cost)

            self.refresh_table()

    def del_item_fromdb(self, itm_id):
        self.inv.del_item(itm_id)

        self.refresh_table()

    def refresh_table(self):
        # Update Table
        if self.search_item.text() != '' and self.search_item.text() is not None:
            self.search_item_indb()
        else:
            self.get_new_items()
