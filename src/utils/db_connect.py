from contextlib import contextmanager
import sqlite3


@contextmanager
def connect(db_path: str):
    """
    Provides a cursor object for executing SQL queries on a database connected
    using SQLite.

    Args:
        db_path (str): path to an existing SQLite database file that the function
            connects to.

    """
    with sqlite3.connect(db_path) as conn:
        yield conn.cursor()
