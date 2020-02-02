#-- code: utf-8 -- 
import re

company_name = "Maharashtra Decorators"
sqllite_db_file = 'db/sqllite.db'
delete_icon = "images/delete.png"
update_icon = "images/update.png"
number_pattern = re.compile(r'[0-9]{1,}\.*[0-9]*')
name_patter = re.compile(r'[A-Za-z0-9\ ]{1,}')
