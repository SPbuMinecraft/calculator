import sqlite3
import datetime


def connect_db(db_filename: str):
    db_connection = sqlite3.connect(db_filename)
    return db_connection


def is_db_open(connection):
    try:
        connection.cursor()
        return True
    except Exception as ex:
        return False


def connect_and_check(db_filename: str):
    connection = connect_db(db_filename)
    if is_db_open(connection):
        return connection, connection.cursor()
    return None, None


def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Calculation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            formula TEXT NOT NULL,
            result TEXT NOT NULL,
            calculation_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)
    ''')

def clean_table(cursor):
    cursor.execute('''
        DELETE FROM Calculation
    ''')


def add_expressions(cursor, expressions, results):
    assert len(expressions) == len(results)
    values_string = ','.join([f"('{expr}', '{res}')" for expr, res in zip(expressions, results)])
    cursor.execute(f'''
        INSERT INTO Calculation (formula, result)
        VALUES {values_string}
    ''')


def get_history(cursor):
    res = cursor.execute('''
        SELECT formula, result FROM Calculation
    ''')
    return res.fetchall()


def disconnect_db(db_connection):
    db_connection.commit()
    db_connection.close()


class SQLWorker:
    def __init__(self, db_filename: str, buffer_size: int = 1, clear_file: bool = True):
        self.db_filename = db_filename
        self.buffer_size = buffer_size
        self.lines: list[list[str]] = []

        connection, cursor = connect_and_check(db_filename)
        if not connection:
            raise ConnectionError("Can not connect to the database!")

        create_table(cursor)
        if clear_file:
            clean_table(cursor)
        disconnect_db(connection)

    def add_line(self, line: list[str]):
        self.lines.append(line)
        if len(self.lines) == self.buffer_size:
            self.update_table()
            self.lines = []

    def update_table(self):
        connection, cursor = connect_and_check(self.db_filename)
        if not connection:
            raise ConnectionError("Can not connect to the database!")
        add_expressions(cursor, [line[0] for line in self.lines], [line[1] for line in self.lines])
        disconnect_db(connection)
    
    def get_lines(self):
        connection, cursor = connect_and_check(self.db_filename)
        if not connection:
            raise ConnectionError("Can not connect to the database!")
        res = get_history(cursor)
        disconnect_db(connection)
        return res
                