#-- code: utf-8 -- 
from vars import sqllite_db_file, delete_icon, update_icon
from database import BillDB
import tkinter as tk
from tkinter import messagebox as msgbox
from custom import ScrollableFrame

## Object of Bill Database
inventory_db = BillDB(sqllite_db_file)
inventory_db.create_table()

def admin_portal():
    """ """
    # Define Custom Actions
    def add_item_in_inventory(name, cost):
        try:
            inventory_db.add_item(name, float(cost))
        except:
            msgbox.showinfo("Error", "Unable to insert provided item")
        bill_items.destroy()
        item_listing_widget()

    def delete_item_from_inventory(id):
        try:
            inventory_db.del_item(int(id))
        except:
            msgbox.showinfo("Error", "Cannot Delete selected Item")
        bill_items.destroy()
        item_listing_widget()

    def update_cost_in_inventory(id, cost):
        inventory_db.update_cost(int(id), float(cost))
        #try:
        #    inventory_db.update_cost(int(id), float(cost))
        #except:
        #    msgbox.showinfo("Error", "Cannot Delete selected Item")
        bill_items.destroy()
        item_listing_widget()

    def item_adding_widget():
        global add_item
        add_item = tk.LabelFrame(admin_page, text = "Add Item")
        add_item.pack(anchor = tk.N, side = tk.TOP, fill = "x", padx = 5, pady = 5)

        tk.Label(add_item, text = "Item Name: ").pack(anchor = "n", side = tk.LEFT)
        i_name = tk.Entry(add_item)
        i_name.pack(anchor = "n", side = tk.LEFT)

        tk.Label(add_item, text = "Item Cost: ").pack(anchor = "n", side = tk.LEFT)
        i_cost = tk.Entry(add_item)
        i_cost.pack(anchor = "n", side = tk.LEFT)

        tk.Button(add_item, text = "Add Item", command = \
            lambda: add_item_in_inventory(i_name.get(), i_cost.get()))\
                .pack(anchor = "n", side = tk.RIGHT, fill = "y", pady = 5, padx = 5)
    
    def item_listing_widget():
        global bill_items
        bill_items = tk.LabelFrame(admin_page, text = "Available Items")
        bill_items.pack(anchor = tk.N, side = tk.BOTTOM, fill = "both", expand = "yes", padx = 5, pady = 5)

        item_list_wraper = ScrollableFrame(bill_items)
        item_list_wraper.pack(anchor = tk.N, fill = "both", expand = "yes", padx = 5, pady = 5)

        # Wrap Header
        tk.Label(item_list_wraper.scroll_frame, text = "Item")\
            .grid(row = 0, column = 1, padx = 10, pady = 2, sticky = "w")
        tk.Label(item_list_wraper.scroll_frame, text = "Cost")\
            .grid(row = 0, column = 2, padx = 10, pady = 2, sticky = "w")
        
        # get Inventory Items
        inventory = inventory_db.get_items()

        #del_button = []
        for rowid, item in enumerate(inventory, start = 1):
            item_id, item_name, item_cost = item
            
            # Create Delete item button
            del_icon = tk.PhotoImage(file = delete_icon, master = admin_page)
            del_button = tk.Button(item_list_wraper.scroll_frame, image = del_icon,\
                 height = 20, width = 20, borderwidth = 0,\
                     command = lambda item_id = item_id: delete_item_from_inventory(item_id))
            del_button.image = del_icon
            del_button.grid(row = rowid, column = 0, padx = 10, pady = 2, sticky = "w")

            # Create label for listing Item Name
            tk.Label(item_list_wraper.scroll_frame, text = str(item_name))\
                .grid(row = rowid, column = 1, padx = 10, pady = 2, sticky = "w")

            # Create label for listing Item Cost
            tk.Label(item_list_wraper.scroll_frame, text = str(item_cost))\
                .grid(row = rowid, column = 2, padx = 10, pady = 2, sticky = "w")

            # Tab for spacing
            tk.Label(item_list_wraper.scroll_frame, text = "\t")\
                .grid(row = rowid, column = 3, padx = 10, pady = 2, sticky = "w")

            # Input new Cost
            tk.Label(item_list_wraper.scroll_frame, text = "New Cost: ")\
                .grid(row = rowid, column = 4, padx = 10, pady = 2, sticky = "w")
            
            new_cost = tk.Entry(item_list_wraper.scroll_frame)
            new_cost.grid(row = rowid, column = 5, padx = 10, pady = 2, sticky = "w")

            # Tab for spacing
            tk.Label(item_list_wraper.scroll_frame, text = "\t")\
                .grid(row = rowid, column = 6, padx = 10, pady = 2, sticky = "w")

            # Button to Update Cost
            upd_icon = tk.PhotoImage(file = update_icon, master = admin_page)
            upd_button = tk.Button(item_list_wraper.scroll_frame, image = upd_icon,\
                 height = 20, width = 20, borderwidth = 0,\
                     command = lambda item_id = item_id, cost = new_cost: update_cost_in_inventory(item_id, cost.get()))
            upd_button.image = upd_icon
            upd_button.grid(row = rowid, column = 7, padx = 10, pady = 2, sticky = "w")
        
    # Create Admin page
    admin_page = tk.Tk()
    admin_page.title("Admin")
    admin_page.minsize(width = 1200, height = 600)
    admin_page.geometry("+200+100") #200 from left and 100 pixel from top

    # Create top widget to adding items
    item_adding_widget()

    # Create item listing widget
    item_listing_widget()

    admin_page.mainloop()

if __name__ == "__main__":
    admin_portal()