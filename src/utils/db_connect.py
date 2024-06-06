from contextlib import contextmanager
import sqlite3


@contextmanager
def connect(db_path: str):
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = lambda c, r: dict(
            [(col[0], r[idx]) for idx, col in enumerate(c.description)]
        )
        yield conn.cursor()
