const {BillDB}  = require('./js/database');

var billdb = new BillDB();
billdb.get_all_items();