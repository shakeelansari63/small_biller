#-- code: utf-8 -- 
import sqlite3 as sqldb

class SQLConnection:
    """
    Common class for connecting SQL
    """
    def __init__(self, dbfile):
        self.db_file = dbfile
    
    def run_sql(self, sql):
        try:
            conn = sqldb.connect(self.db_file)
            curr = conn.cursor()
            curr.execute(sql)
            rows = curr.fetchall()
        except:
            rows = None
        finally:
            conn.commit()
            curr.close()
            conn.close()
        return rows
    
    def create_table(self):
        pass

    def drop_table(self):
        pass

    def reset_db(self):
        self.drop_table()
        self.create_table()


class BillDB(SQLConnection):
    """
    Bills Database Class
    """
    def create_table(self):
        sql = """ CREATE TABLE IF NOT EXISTS BILLDATA (
            ITEM_ID integer not null PRIMARY KEY,
            ITEM_NAME text not null UNIQUE,
            ITEM_COST real not null
        )"""
        self.run_sql(sql)

    def drop_table(self):
        sql = """DROP TABLE BILLDATA"""
        self.run_sql(sql)

    def add_item(self, item_name, item_cost):
        sql = """INSERT INTO BILLDATA
        (ITEM_ID, ITEM_NAME, ITEM_COST)
        SELECT COALESCE(MAX(ITEM_ID), 0) + 1
        , '{item_name}', {item_cost}
        FROM BILLDATA""".format(item_name = item_name, item_cost = item_cost)
        self.run_sql(sql)

    def del_item(self, item_id):
        sql = """DELETE FROM BILLDATA
        WHERE ITEM_ID = {}""".format(item_id)
        self.run_sql(sql)

    def get_items(self):
        sql = """SELECT 
        ITEM_ID, ITEM_NAME, ITEM_COST
        FROM BILLDATA
        ORDER BY ITEM_NAME ASC"""
        return self.run_sql(sql)
    
    def get_item_by_name_pattern(self, pattern):
        sql = """SELECT
        ITEM_ID, ITEM_NAME, ITEM_COST
        FROM BILLDATA
        WHERE ITEM_NAME LIKE '%{}%'
        ORDER BY ITEM_NAME ASC""".format(pattern)
        return self.run_sql(sql)

    def get_item_by_id(self, item_id):
        sql = """SELECT 
        ITEM_ID, ITEM_NAME, ITEM_COST
        FROM BILLDATA WHERE ITEM_ID = {}
        """.format(item_id)
        return self.run_sql(sql)

    def update_cost(self, item_id, item_cost):
        sql = """UPDATE
        BILLDATA SET ITEM_COST = {item_cost}
        WHERE ITEM_ID = {item_id}""".format(item_id = item_id, item_cost = item_cost)
        self.run_sql(sql)

class Bill(SQLConnection):
    """
    Current Bills Database Class
    """
    def create_table(self):
        sql = """ CREATE TABLE IF NOT EXISTS CURRENT_BILL (
            LISTING_ID integer not null PRIMARY KEY,
            ITEM_NAME text not null UNIQUE,
            UNIT_ITEM_COST real not null,
            ITEM_QUANTITY integer not null
        )"""
        self.run_sql(sql)
    
    def drop_table(self):
        sql = """DROP TABLE CURRENT_BILL"""
        self.run_sql(sql)

    def add_item(self, item_name, item_cost, item_quantity):
        sql = """ INSERT INTO CURRENT_BILL
        (LISTING_ID, ITEM_NAME, UNIT_ITEM_COST, ITEM_QUANTITY)
        SELECT COALESCE(MAX(LISTING_ID), 0) + 1
        , '{item_name}', {item_cost}, {item_quantity}
        FROM CURRENT_BILL""".format(item_name = item_name, item_cost = item_cost, item_quantity = item_quantity)
        self.run_sql(sql)

    def get_items(self):
        sql = """SELECT LISTING_ID, ITEM_NAME, UNIT_ITEM_COST, ITEM_QUANTITY
        FROM CURRENT_BILL"""
        rows = self.run_sql(sql)
        return rows