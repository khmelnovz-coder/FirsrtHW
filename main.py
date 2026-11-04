import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem
from frontend_main import Ui_MainWindow
from addEditCoffeeForm import Ui_AddEditForm


class AddEditCoffeeForm(QDialog, Ui_AddEditForm):
    def __init__(self, coffee_id=None):
        super().__init__()
        self.setupUi(self)
        self.coffee_id = coffee_id
        if self.coffee_id is not None:
            self.load_coffee_data()

        self.saveButton.clicked.connect(self.save_data)

    def load_coffee_data(self):
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, roast_level, type, taste_description, price, package_size FROM coffee WHERE id = ?",
            (self.coffee_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            self.nameInput.setText(row[0])
            self.roastInput.setText(row[1])
            self.typeInput.setText(row[2])
            self.tasteInput.setText(row[3])
            self.priceInput.setValue(row[4])
            self.sizeInput.setValue(row[5])

    def save_data(self):
        name = self.nameInput.text()
        roast = self.roastInput.text()
        coffee_type = self.typeInput.text()
        taste = self.tasteInput.text()
        price = self.priceInput.value()
        size = self.sizeInput.value()

        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()

        if self.coffee_id is None:

            cursor.execute('''
                           INSERT INTO coffee (name, roast_level, type, taste_description, price, package_size)
                           VALUES (?, ?, ?, ?, ?, ?)
                           ''', (name, roast, coffee_type, taste, price, size))
        else:

            cursor.execute('''
                           UPDATE coffee
                           SET name              = ?,
                               roast_level       = ?,
                               type              = ?,
                               taste_description = ?,
                               price             = ?,
                               package_size      = ?
                           WHERE id = ?
                           ''', (name, roast, coffee_type, taste, price, size, self.coffee_id))

        conn.commit()
        conn.close()
        self.accept()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_db()
        self.load_db()

        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)

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

    def add_coffee(self):

        form = AddEditCoffeeForm()
        if form.exec():
            self.load_db()

    def edit_coffee(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            return

        coffee_id = int(self.tableWidget.item(selected_row, 0).text())

        form = AddEditCoffeeForm(coffee_id)
        if form.exec():
            self.load_db()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
