# FriDB
A simple single-file-base database operating on a JSON file. 
Does not support SQL.

## Table of Contents
- [Overview](#overview)
- [Example](#example)
- [Database access methods](#database-access-methods)
    - [create](#create)
    - [connect](#connect)
    - [disconnect](#disconnect)
    - [create_table](#create_table)
    - [tables](#tables)
    - [drop_table](#drop_table)
    - [save](#save)
    - [read](#read)
    - [insert](#insert)
    - [delete](#delete)
    - [update](#update)
- [Testing](#testing)
- [Links](#links)

## Overview

## Example
The example creates a simple database to store customers and orders in a shop.
```python
import fridb

# create a new database with two tables in it
db = fridb.create('shop.db')
db.create_table('customers')
db.create_table('orders')

# insert an order and a customer
db.insert('customers', 'John Smith')
db.insert('orders', 'item #1')
db.insert('orders', 'item #2')

# insert another order and a new customer
db.insert('customers', 'Julia Miller')
db.insert('orders', 'item #1')

# print the last two orders
print(db.read('orders', limit=-2))
```
In reality you should add something like an ID to each data set in order to be
able to differentiate between those sets. But for a short demonstration this
should be enough.

## Database access methods
This section gives you a short overview what methods to interact with the
database are available and how they can be used.
### create
This function creates a new database with no entries or tables in it. You have
to specify a file, where the database is stored to. Note that an existing
database with the same filename is overridden.

It returns a FriDB object, that can be used to interact with the database.

### connect
This function connects to an existing database. If there is no database file at
the path available or the file is empty a new database is created. The existing
content is loaded into the memory database.

It returns a FriDB object, that can be used to interact with the database.

### disconnect
This method closes the connection to the database. The data is written to the
database file and the file is closed. After a call to this method there is no
access to the data in the database and every other call to a public method of
the object fails.

Note that you have to call at least either disconnect() or save() to store the
database state or your data will be lost. Although a call to save() and one to
close() on the file descriptor does nearly the same work it is recommended to
use disconnect().

### create_table
This method creates a new table, that can hold database entries. It can take
any string as its name.

At least one table is required if any data should be stored in the database.

This is the equivalent to the SQL command `CREATE TABLE ...`.

### tables
This method returns a list of all tables that are stored inside the database.

This is the equivalent to the SQL command `SHOW TABLES;`.

### drop_table
This method deletes an entire table and all of its entries.

Note that the change is not directly written to the file but stored in the
memory. The change is written if save() or disconnect() is called.

This is the equivalent to the SQL command `DROP TABLE ...`.

### save
This method writes the changes made to the database (which are done only in the
memory) to the database file. 

Note that you have to call at least either disconnect() or save() to store the
database state or your data will be lost. Although a call to save() and one to
close() on the file descriptor does nearly the same work it is recommended to
use disconnect().

### read
This method returns a list of all entries in a table. The number of returned
entries can be unlimited (limit=0, default) or limited to the first n (limit>0)
or the last n entries (limit<0).

This is roughly equivalent to the SQL 
`SELECT * FROM ... [SORT ASC|DESC] [LIMIT ]` statement, but you can only
query all statements, with the option to limit the number of rows returned.
Currently you cannot specify a filter in the statement.

### insert
Insert a new data set into a table. It is always inserted at the end of the
table entries.

Note that the change is not directly written to the file but stored in the
memory. The change is written if save() or disconnect() is called.

This is the equivalent to the SQL command `INSERT ... INTO TABLE ...`.

### delete
This is not implemented yet.

### update
This is not implemented yet.

## Testing
The module is tested using the python module 'doctest'. The docstrings for the
module and some functions include the docstring tests. All methods of the
class FriDB are tested in the module test, but they don't have a test in their
own docstrings.

To invoke the tests type the following command in the directory with the file
fridb.py:
```bash
$ python -m doctest fridb.py
```
Alternatively you can add the flag `--verbose` to get more information about
the tests.

## Links
The [FriServer](https://github.com/jfrimmel/FriServer) project uses this 
database in one of its plug-ins.