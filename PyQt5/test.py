#-- code: utf-8 -- 
from vars import *
from database import *
import tkinter as tk

bill_db = BillDB()
bill_db.reset_db()
bill_db.add_item('Baans','5')
bill_db.add_item('Balli','20')
bill_db.add_item('Chair','20')
bill_db.add_item('Glass','20')
bill_db.add_item('Jhummar','5')
bill_db.add_item('Plate','20')
bill_db.add_item('Table','20')
print(bill_db.get_items())
#print(bill_db.get_item_by_id(1))

bill_item = Bill()
bill_item.reset_db()
bill_item.add_item('Baans','5', 5)
bill_item.add_item('Balli','20', 10)
bill_item.add_item('Chair','20', 2)
bill_item.add_item('Glass','20', 12)
bill_item.add_item('Jhummar','5', 22)
print(bill_item.get_items())