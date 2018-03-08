"""
Provide a simple single-file-base database.

Usage:
    The basic usage is very simple: you have to import this module. After that
    you can either connect to a existing database or create a new one and store
    the return value in a variable, which you can use to interact with the
    database. 
    You can insert data sets and read the existing ones back. You may limit the
    number of data sets to read using the optional parameter 'limit'.

Example:
    import fridb

    db = fridb.create()
    db.insert('a string')
    db.insert('a second string')
    result = db.read()
    only_the_fist_row = db.read(limit=1)[0]
    db.disconnect()

Tests:
    You can find rudimentary tests of the database in this section. Each set of
    test is prefixed with a short explanation what is tested an why.

    A newly created database has no entries in it.
    >>> db = create('test.db')
    >>> len(db.read())
    0
    
    If an data set is inserted, the number of returned rows is incremented by one.
    The database returns exactly the inserted string.
    >>> db.insert('hello, world!')
    >>> len(db.read())
    1
    >>> db.read()[0]
    'hello, world!'
    
    Test the limit option and ensure that the data sets are returned on the right
    order.
    >>> db.insert('2nd string')
    >>> len(db.read())
    2
    >>> len(db.read(1))
    1
    >>> len(db.read(-1))
    1
    >>> db.read()[0]
    'hello, world!'
    >>> db.read()[1]
    '2nd string'
    >>> db.read(-1)[0]
    '2nd string'
    
    Ensure that the file object is closed, if the database connection is closed.
    All calls to the public methods of the database object except for disconnect()
    are raising exceptions after that point. disconnect() has no effect in that
    case.
    >>> db.disconnect()
    >>> db.insert('should not be inserted')
    Traceback (most recent call last):
      ...
    fridb.DBError: Database file is closed
    >>> db.read()
    Traceback (most recent call last):
      ...
    fridb.DBError: Database file is closed
    >>> db.disconnect()
    
    
    >>> db = connect('test.db')
"""
import os
import json

def connect(db_file):
    """Connect to a database file."""
    fp = open(str(db_file), 'a+')
    return FriDB(fp)

def create(db_file):
    """Creates an empty database."""
    fp = open(str(db_file), 'a+')
    return FriDB(fp)

class FriDB:
    """A simple JSON-based database."""

    def __init__(self, fp):
        """
        Construct the database object.
        
        This method takes an open file pointer. At first it checks, if the
        passed parameter is in fact open and raises an exception if not. If the
        file is open and the file-size is zero a new database file is created,
        otherwise the existing one is loaded.
        
        Note, that it is recommended to use one of the two functions
        'fridb.connect()' or 'fridb.create()' instead of creating an object of
        this class directly. Those two functions do everything needed to have
        access to a database of a given file.
        :param fp: A open file object to the database file.
        """
        self._file = fp
        self._check_fp()
        self._rows = None
        if _get_file_size(fp) == 0:
            self._create_new_db()
        else:
            self._load_db()

    def _create_new_db(self):
        """Create a new database into an empty file."""
        self._rows = []

    def _load_db(self):
        """Load the database from an existing file."""
        data = json.load(self._file)
        print(data)
        # TODO

    def _check_fp(self):
        """Check, if the file is still open and raise an exception if not."""
        if self._file.closed:
            raise DBError('Database file is closed')

    def insert(self, object):
        """
        Insert one data set into a row of the database.

        The object is inserted as a string, so if you want to store an object,
        you will have to serialize it before (e.g. using the JSON format).
        The object takes a whole row for its own.
        :param object: The object to store.
        """
        self._check_fp()
        self._rows.append(object)

    def read(self, limit=0):
        """
        Read the entries from the database.

        The method returns an array of up to 'limit' rows. There are three
        possible cases for the limit:
        1. If the limit is zero all rows are returned.
        2. If the limit is positive the first n rows are returned.
        3. If the limit is negative the last n rows are returned.
        :param limit: This optional parameter specifies the maximum number of
        rows returned.
        :return: An array of strings containing the stored data.
        :rtype: string array
        """
        self._check_fp()
        if limit < 0:
            return self._rows.copy()[limit:]
        elif limit > 0:
            return self._rows.copy()[:limit]
        else:
            return self._rows.copy()
    
    def disconnect(self):
        """Disconnect for the database file and close the file object."""
        self._file.close()

def _get_file_size(fp):
    """Return the size of a file in bytes."""
    return os.fstat(fp.fileno()).st_size

class DBError(Exception):
    """Custom exception thrown from the class FriDB."""
