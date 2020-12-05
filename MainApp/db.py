import sqlite3 as db
from .setting import setting
from datetime import datetime


class BaseDB:
    def __init__(self):
        self.dbfile = setting['appdb']

        # Create table is not exist
        self.create_table()

    def runsql(self, sql):
        # print(sql)
        try:
            conn = db.connect(self.dbfile)
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
        except Exception as e:
            print(e)
            rows = []
        finally:
            conn.commit()
            cur.close()
            conn.close()
        return rows

    def create_table(self):
        pass

    def drop_table(self):
        pass

    def reset_db(self):
        self.drop_table()
        self.create_table()


class Inventory(BaseDB):

    # Define Table structure
    def create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS INVENTORY (
        ITEM_ID integer not null PRIMARY KEY,
        ITEM_NAME text not null UNIQUE,
        ITEM_COST real not null
        )"""

        self.runsql(sql)

    def drop_table(self):
        sql = """
        DROP TABLE INVENTORY
        """

        self.runsql(sql)

    def add_item(self, item_name, item_cost):
        sql = """INSERT INTO INVENTORY
        (ITEM_ID, ITEM_NAME, ITEM_COST)
        SELECT COALESCE(MAX(ITEM_ID), 0) + 1
        , '{item_name}', {item_cost}
        FROM INVENTORY""".format(item_name=item_name, item_cost=item_cost)

        self.runsql(sql)

    def del_item(self, item_id):
        sql = """DELETE FROM INVENTORY
        WHERE ITEM_ID = {}""".format(item_id)

        self.runsql(sql)

    def get_items(self):
        sql = """SELECT
        ITEM_ID, ITEM_NAME, ITEM_COST
        FROM INVENTORY
        ORDER BY ITEM_ID DESC
        LIMIT 50"""

        return self.runsql(sql)

    def get_item_by_name_pattern(self, pattern):
        sql = """SELECT
        ITEM_ID, ITEM_NAME, ITEM_COST
        FROM INVENTORY
        WHERE ITEM_NAME LIKE '%{}%'
        ORDER BY ITEM_ID DESC
        LIMIT 50""".format(pattern)

        return self.runsql(sql)

    def get_item_by_name(self, name):
        sql = """SELECT
        ITEM_ID, ITEM_NAME, ITEM_COST
        FROM INVENTORY
        WHERE ITEM_NAME = '{}'
        ORDER BY ITEM_ID DESC""".format(name)

        return self.runsql(sql)

    def get_item_by_id(self, item_id):
        sql = """SELECT
        ITEM_ID, ITEM_NAME, ITEM_COST
        FROM INVENTORY WHERE ITEM_ID = {}
        """.format(item_id)

        return self.runsql(sql)

    def update_cost(self, item_id, item_cost):
        sql = """UPDATE INVENTORY 
        SET ITEM_COST = {item_cost}
        WHERE ITEM_ID = {item_id}""".format(item_id=item_id, item_cost=item_cost)

        self.runsql(sql)


class Bill(BaseDB):
    # Define table structure
    def create_table(self):
        sql = """ CREATE TABLE IF NOT EXISTS CURRENT_BILL (
            LISTING_ID integer not null PRIMARY KEY,
            ITEM_NAME text not null UNIQUE,
            UNIT_ITEM_COST real not null,
            ITEM_QUANTITY integer not null,
            NO_OF_DAYS integer
        )"""
        self.runsql(sql)

    def drop_table(self):
        sql = """DROP TABLE CURRENT_BILL"""
        self.runsql(sql)

    def add_item(self, item_name, item_cost, item_quantity, days):
        sql = """ INSERT INTO CURRENT_BILL
        (LISTING_ID, ITEM_NAME, UNIT_ITEM_COST, ITEM_QUANTITY, NO_OF_DAYS)
        SELECT COALESCE(MAX(LISTING_ID), 0) + 1
        , '{item_name}', {item_cost}, {item_quantity}, {days}
        FROM CURRENT_BILL""".format(item_name=item_name, item_cost=item_cost, item_quantity=item_quantity, days=days)
        self.runsql(sql)

    def get_items(self):
        sql = """SELECT LISTING_ID, ITEM_NAME, UNIT_ITEM_COST, ITEM_QUANTITY, NO_OF_DAYS
        FROM CURRENT_BILL
        ORDER BY LISTING_ID"""
        rows = self.runsql(sql)
        return rows

    def del_item(self, item_listing_id):
        sql = """DELETE FROM CURRENT_BILL
        WHERE LISTING_ID = {}""".format(item_listing_id)
        self.runsql(sql)


class BillHist(BaseDB):
    """ Bill History Database"""

    def create_table(self):
        sql = """CREATE TABLE IF NOT EXISTS BILL_HIST(
            BILL_ID INTEGER,
            CUSTOMER_NAME TEXT,
            CUSTOMER_PHONE TEXT,
            DELIVERY_ADDRESS TEXT,
            ITEMS TEXT,
            TOTAL_BILL_AMT REAL,
            DELIVERY_DATE DATETIME,
            UPDATE_DATE DATETIME
        )"""

        self.runsql(sql)

    def drop_table(self):
        sql = """DROP TABLE BILL_HIST"""

        self.runsql(sql)

    def save_bill(self, cust_name, cust_phone, dlvry_addr, items, total_bill_amt, dlvry_date):
        sql = """INSERT INTO BILL_HIST(
            BILL_ID,
            CUSTOMER_NAME,
            CUSTOMER_PHONE,
            DELIVERY_ADDRESS,
            ITEMS,
            TOTAL_BILL_AMT,
            DELIVERY_DATE,
            UPDATE_DATE
        ) SELECT
            COALESCE(MAX(BILL_ID), 0) + 1,
            '{}',
            '{}',
            '{}',
            '{}',
             {} ,
            '{}',
            '{}'
          FROM BILL_HIST""".format(cust_name, cust_phone, dlvry_addr, items,
                                   total_bill_amt, dlvry_date, datetime.now())

        self.runsql(sql)

    def update_bill(self, bill_id, cust_name, cust_phone, dlvry_addr, items, total_bill_amt, dlvry_date):
        sql = """UPDATE BILL_HIST
            SET CUSTOMER_NAME = '{}',
                CUSTOMER_PHONE = '{}',
                DELIVERY_ADDRESS = '{}',
                ITEMS = '{}',
                TOTAL_BILL_AMT = {},
                DELIVERY_DATE = '{}',
                UPDATE_DATE = '{}'
            WHERE BILL_ID = {}
        """.format(cust_name, cust_phone, dlvry_addr, items,
                   total_bill_amt, dlvry_date, datetime.now(), bill_id)

        self.runsql(sql)

    def delete_bill(self, bill_id):
        sql = """DELETE FROM BILL_HIST
            WHERE BILL_ID = {}""".format(bill_id)

        self.runsql(sql)

    def get_bill_by_id(self, bill_id):
        sql = """SELECT
            BILL_ID,
            CUSTOMER_NAME,
            CUSTOMER_PHONE,
            DELIVERY_ADDRESS,
            ITEMS,
            TOTAL_BILL_AMT,
            DELIVERY_DATE,
            UPDATE_DATE
        FROM BILL_HIST
        WHERE BILL_ID = {}""".format(bill_id)

        return self.runsql(sql)

    def search_bill(self, search_txt):
        sql = """SELECT 
            BILL_ID,
            CUSTOMER_NAME,
            CUSTOMER_PHONE,
            DELIVERY_ADDRESS,
            ITEMS,
            TOTAL_BILL_AMT,
            DELIVERY_DATE,
            UPDATE_DATE
        FROM BILL_HIST
        WHERE TRIM(CUSTOMER_NAME) || TRIM(DELIVERY_ADDRESS) LIKE '%{}%'
        ORDER BY CUSTOMER_NAME
        LIMIT 50""".format(search_txt)

        return self.runsql(sql)
