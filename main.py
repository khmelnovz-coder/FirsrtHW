import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6 import uic
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("main.ui", self)
        self.init_db()
        self.load_db()

    def init_db(self):
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS coffee
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           name
                           TEXT,
                           roast_level
                           TEXT,
                           type
                           TEXT,
                           taste_description
                           TEXT,
                           price
                           REAL,
                           package_size
                           REAL
                       )
                       ''')

        cursor.execute("SELECT COUNT(*) FROM coffee")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                           INSERT INTO coffee (name, roast_level, type, taste_description, price, package_size)
                           VALUES ('Арабика Эфиопия', 'Средняя', 'В зернах', 'Цитрусовые нотки, мягкий вкус', 450.0,
                                   0.25)
                           ''')
            conn.commit()

        conn.close()

    def load_db(self):
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, roast_level, type, taste_description, price, package_size FROM coffee")
        rows = cursor.fetchall()

        table = self.findChild(object, 'tableWidget')
        if table:
            table.setRowCount(len(rows))

            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
