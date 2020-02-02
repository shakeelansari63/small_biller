const sqlite = require('sqlite3');

class BillDB{
    constructor(){
        this.billdb = new sqlite.Database('db/billdb.db');
        this.billdb.run("CREATE TABLE IF NOT EXISTS BILLDATA (\
            ITEM_ID integer not null PRIMARY KEY,\
            ITEM_NAME text not null UNIQUE,\
            ITEM_COST real not null\
        )");
    }

    get_all_items(){
        return this.billdb.all(
            "SELECT ITEM_ID, ITEM_NAME, ITEM_COST FROM BILLDATA"
        )
    }
}

// testing
var billdb = new BillDB();
console.log(billdb.get_all_items());