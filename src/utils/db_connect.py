from contextlib import contextmanager
import sqlite3


@contextmanager
def connect(db_path: str):
    with sqlite3.connect(db_path) as conn:
        yield conn.cursor()
