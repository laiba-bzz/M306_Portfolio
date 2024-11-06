import sqlite3
from green_item import GreenItem


class GreenApp:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()
