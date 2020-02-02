#-- code: utf-8 -- 
from vars import sqllite_db_file, company_name, bill_seperator
from database import BillDB, Bill
from admin import admin_portal, inventory_db
import tkinter as tk
from tkinter import messagebox as msgbox
from custom import ScrollableFrame
import re

my_bill = Bill(sqllite_db_file)
#my_bill.reset_db()

def main_page():
    """ """
    # Define function to refresh on searching 
    def filter_item_list(search_key):
        item_add_frame.destroy()
        add_item_window(search_key)
        return True

    def create_new_bill():
        global my_bill
        my_bill.reset_db()
        bill_detail_frame.destroy()
        bill_detail_window()

    
    # Define function to add item to bill
    def add_item_to_current_bill(item_list_wg, item_quanty_wg):
        # Get the Input item from list
        try:
            item = item_list_wg.selection_get()
        except:
            item = ""
        
        # Get the quantities
        quantity = item_quanty_wg.get()

        # Edge Case check
        if item == "":
            msgbox.showerror("Error", "Select Some Item")
        elif quantity == "":
            msgbox.showerror("Error", "Provide Correct Quantity")
        else:
            # Extract Item Name from List
            item_name = re.compile(r'(.*?)\s\-\s\(\s[0-9\.]*?\seach\)').findall(item)[0]

            # Extract Item cast from list
            item_cost = re.compile(r'.*?\s\-\s\(\s([0-9\.]*?)\seach\)').findall(item)[0]

            my_bill.add_item(item_name, item_cost, quantity)
            bill_detail_frame.destroy()
            bill_detail_window()
            item_add_frame.destroy()
            add_item_window(search_box.get())

    # Define top tab for searching Item
    def search_items_pane():
        global search_widget
        search_widget = tk.Frame(bill_frame_container)
        search_widget.pack(anchor = tk.N, side = tk.TOP, fill = "x", padx = 5, pady = 5)

        # Search Input with validation to refresh item list
        tk.Label(search_widget, text = "Search: ")\
            .pack(anchor = tk.N, side = tk.LEFT)
        global search_box
        search_box = tk.Entry(search_widget)
        search_box.configure(validate = "key", validatecommand = (search_box.register(filter_item_list), '%P'))
        search_box.pack(anchor = tk.N, side = tk.LEFT)

        # Button to refresh Items List
        tk.Button(search_widget, text = "Refresh", command = lambda : filter_item_list(search_box.get()))\
            .pack(anchor = tk.N, side = tk.RIGHT)
        
        # Spacer
        tk.Label(search_widget, text = "    ").pack(anchor = tk.N, side = tk.RIGHT)

        # Button to refresh and create new bill
        tk.Button(search_widget, text = "New Bill", command = create_new_bill)\
            .pack(anchor = tk.N, side = tk.RIGHT)

    # Define Left tab for adding items to bill
    def add_item_window(search_key = ''):
        global item_add_frame
        item_add_frame = tk.LabelFrame(bill_frame_box, text = "Add Items")
        item_add_frame.pack(side = tk.LEFT, fill = "both", padx = 5, pady = 5)

        # Generate Inventory Listing
        if search_key == "":
            inventory = inventory_db.get_items()
        else:
            inventory = inventory_db.get_item_by_name_pattern(search_key)

        scroll_list = tk.Frame(item_add_frame)
        scroll_list.pack(side = tk.TOP, fill = "both", expand = "yes", padx = 5, pady = 5)

        scroll_bar = tk.Scrollbar(scroll_list)
        scroll_bar.pack(side = tk.RIGHT, fill = 'y')

        items_list = tk.Listbox(scroll_list, yscrollcommand = scroll_bar.set)
        items_list.pack(side = tk.LEFT, fill = "both", expand = "yes", padx = 5, pady = 5)

        scroll_bar.config( command = items_list.yview )
        for num, item in enumerate(inventory):
            _, item_name, item_cost = item
            list_display = item_name + " - ( " + str(item_cost) + " each)"
            items_list.insert(num, list_display)
        items_list.selection_set(0)

        item_list_action = tk.Frame(item_add_frame)
        item_list_action.pack(side = tk.BOTTOM, fill = "both", expand = "yes", padx = 5, pady = 5)

        tk.Label(item_list_action, text = "Quantity: ").grid(row = 0, column = 0)
        item_quantity_inp = tk.Entry(item_list_action)
        item_quantity_inp.grid(row = 0, column = 1)

        tk.Button(item_list_action, text = "Add to Bill", \
            command = lambda : add_item_to_current_bill(items_list, item_quantity_inp) \
                ).grid(row = 1, column = 0, columnspan = 2, sticky = tk.W)

    # Define right tab for bill detail
    def bill_detail_window():
        global bill_detail_frame
        bill_detail_frame = tk.LabelFrame(bill_frame_box, text = "Bill Details")
        bill_detail_frame.pack(side = tk.RIGHT, fill = "both", expand = "yes", padx = 5, pady = 5)

        global bill_list_frame
        bill_list_frame = ScrollableFrame(bill_detail_frame, bg = "White")
        bill_list_frame.pack(fill = "both", expand = "yes", padx = 5, pady = 5)

        # Header in Bill
        tk.Label(bill_list_frame.scroll_frame, text = company_name, bg = "White", fg = "Black", font = ("Arial", 18))\
            .grid(row = 0, column = 0, columnspan = 7)
        tk.Label(bill_list_frame.scroll_frame, text = bill_seperator, bg = "White", fg = "Black", font = ("Arial"))\
            .grid(row = 1, column = 0, columnspan = 7)
        
        tk.Label(bill_list_frame.scroll_frame, text = "Name", bg = "White", fg = "Black", font = ("Arial"))\
            .grid(row = 2, column = 0, sticky = tk.W)
        tk.Label(bill_list_frame.scroll_frame, text = "  |  ", bg = "White", fg = "Black", font = ("Arial"))\
            .grid(row = 2, column = 1)
        tk.Label(bill_list_frame.scroll_frame, text = "Unit Cost", bg = "White", fg = "Black", font = ("Arial"))\
            .grid(row = 2, column = 2, sticky = tk.W)
        tk.Label(bill_list_frame.scroll_frame, text = "  |  ", bg = "White", fg = "Black", font = ("Arial"))\
            .grid(row = 2, column = 3)
        tk.Label(bill_list_frame.scroll_frame, text = "Quantity", bg = "White", fg = "Black", font = ("Arial"))\
            .grid(row = 2, column = 4, sticky = tk.W)
        tk.Label(bill_list_frame.scroll_frame, text = "  |  ", bg = "White", fg = "Black", font = ("Arial"))\
            .grid(row = 2, column = 5)
        tk.Label(bill_list_frame.scroll_frame, text = "Cost", bg = "White", fg = "Black", font = ("Arial"))\
            .grid(row = 2, column = 6, sticky = tk.W)

        tk.Label(bill_list_frame.scroll_frame, text = bill_seperator, bg = "White", fg = "Black", font = ("Arial"))\
            .grid(row = 3, column = 0, columnspan = 7)
        total_bill_amount = 0
        bill_items_in_db = my_bill.get_items()
        for num, item in enumerate(bill_items_in_db, start = 4):
            _, item_name, item_unit_cost, item_qty = item

            total_item_cost = float(item_unit_cost) * int(item_qty)
            total_bill_amount = total_bill_amount + total_item_cost
            tk.Label(bill_list_frame.scroll_frame, text = item_name, bg = "White", fg = "Black", font = ("Arial"))\
                .grid(row = num, column = 0, sticky = tk.W)
            tk.Label(bill_list_frame.scroll_frame, text = "   ", bg = "White", fg = "Black", font = ("Arial"))\
                .grid(row = num, column = 1)
            tk.Label(bill_list_frame.scroll_frame, text = item_unit_cost, bg = "White", fg = "Black", font = ("Arial"))\
                .grid(row = num, column = 2, sticky = tk.W)
            tk.Label(bill_list_frame.scroll_frame, text = "   ", bg = "White", fg = "Black", font = ("Arial"))\
                .grid(row = num, column = 3)
            tk.Label(bill_list_frame.scroll_frame, text = item_qty, bg = "White", fg = "Black", font = ("Arial"))\
                .grid(row = num, column = 4, sticky = tk.W)
            tk.Label(bill_list_frame.scroll_frame, text = "   ", bg = "White", fg = "Black", font = ("Arial"))\
                .grid(row = num, column = 5)
            tk.Label(bill_list_frame.scroll_frame, text = total_item_cost, bg = "White", fg = "Black", font = ("Arial"))\
                .grid(row = num, column = 6, sticky = tk.W)
        
        # Trailer
        last_num = len(bill_items_in_db) + 4
        tk.Label(bill_list_frame.scroll_frame, text = bill_seperator, bg = "White", fg = "Black", font = ("Arial"))\
            .grid(row = last_num, column = 0, columnspan = 7)
        
        tk.Label(bill_list_frame.scroll_frame, text = "Total Bill:", bg = "White", fg = "Black", font = ("Arial"))\
            .grid(row = last_num + 1, column = 0, columnspan = 6, sticky = tk.E)
        
        tk.Label(bill_list_frame.scroll_frame, text = total_bill_amount, bg = "White", fg = "Black", font = ("Arial"))\
            .grid(row = last_num + 1, column = 6, sticky = tk.W)

        tk.Label(bill_list_frame.scroll_frame, text = bill_seperator, bg = "White", fg = "Black", font = ("Arial"))\
            .grid(row = last_num + 2, column = 0, columnspan = 7)

    # Define Bottom bar for admin button
    def admin_button():
        action_box = tk.Frame(main_page)
        action_box.pack(anchor = tk.S, side = tk.BOTTOM, fill = "both", padx = 5, pady = 5)

        admin_button = tk.Button(action_box, text = "Update Inventory", command = admin_portal)
        admin_button.pack(side = tk.LEFT)

        #tk.Button(action_box, text = "Print Bill", \
        #    command = lambda: bill_list_frame.generate_pdf())\
        #        .pack(side = tk.RIGHT)
    
    # Make Main Page
    main_page = tk.Tk()
    main_page.title(company_name)
    main_page.minsize(width = 1200, height = 800)
    main_page.geometry("+100+100") #100 from left and 100 pixel from top

    # Making Frame Boxes
    bill_frame_container = tk.LabelFrame(main_page, text = company_name)
    bill_frame_container.pack(anchor = tk.N, side = tk.TOP, fill = "both", expand = "yes", padx = 5, pady = 5)

    # Create Search Item frame
    search_items_pane()

    bill_frame_box = tk.Frame(bill_frame_container)
    bill_frame_box.pack(anchor = tk.N, side = tk.TOP, fill = "both", expand = "yes", padx = 5, pady = 5)

    # Create Add Item window
    add_item_window()

    # Create Bill detail window
    bill_detail_window()

    # Create bottom bar with buttons
    admin_button()

    # Open in Full Screen
    main_page.attributes('-zoomed', True)
    main_page.mainloop()

if __name__ == "__main__":
    main_page()