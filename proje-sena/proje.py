import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTableWidget, \
    QTableWidgetItem, QDialog, QFormLayout, QLabel, QDateEdit, QHBoxLayout, QMessageBox, QComboBox, QColorDialog
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QColor

class Task:
    def __init__(self, title, description, start_date, end_date):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date

class TaskDetailsWindow(QDialog):
    def __init__(self, task, parent=None):
        super(TaskDetailsWindow, self).__init__(parent)
        self.setWindowTitle("Görev Detayları")
        layout = QFormLayout()

        self.title_label = QLabel(f"Başlık: {task.title}")
        self.description_label = QLabel(f"Açıklama: {task.description}")
        self.start_date_label = QLabel(f"Başlangıç Tarihi: {task.start_date}")
        self.end_date_label = QLabel(f"Bitiş Tarihi: {task.end_date}")

        layout.addWidget(self.title_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.end_date_label)

        self.setLayout(layout)

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Yap")
        self.setFixedSize(400, 300)  # Pencereyi büyütüyoruz
        self.layout = QFormLayout()

        self.username_input = QLineEdit(self)
        self.layout.addRow("Kullanıcı Adı:", self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addRow("Şifre:", self.password_input)

        self.login_button = QPushButton("Giriş Yap")
        self.layout.addWidget(self.login_button)
        self.login_button.clicked.connect(self.check_credentials)

        self.register_button = QPushButton("Kaydol")
        self.layout.addWidget(self.register_button)
        self.register_button.clicked.connect(self.open_register_dialog)

        self.setLayout(self.layout)

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()
        # Burada kullanıcı adı ve şifre kontrolü yapılabilir
        self.accept()

    def open_register_dialog(self):
        register_dialog = RegisterDialog(self)
        register_dialog.exec_()

class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kayıt Ol")
        self.setFixedSize(400, 300)  # Pencereyi büyütüyoruz
        self.layout = QFormLayout()

        self.username_input = QLineEdit(self)
        self.layout.addRow("Kullanıcı Adı:", self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addRow("Şifre:", self.password_input)

        self.register_button = QPushButton("Kaydol")
        self.layout.addWidget(self.register_button)
        self.register_button.clicked.connect(self.register_user)

        self.setLayout(self.layout)

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        # Burada veritabanına kullanıcı kaydı yapılabilir
        self.accept()

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ayarlar")
        self.layout = QVBoxLayout()

        # Kullanıcı adı ve şifre değiştirme
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Yeni Kullanıcı Adı")
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Yeni Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.save_button = QPushButton("Kaydet")
        self.save_button.clicked.connect(self.save_changes)
        self.layout.addWidget(self.save_button)

        # Tema seçme butonu
        self.theme_button = QPushButton("Tema Seç")
        self.theme_button.clicked.connect(self.select_theme)
        self.layout.addWidget(self.theme_button)

        self.setLayout(self.layout)

    def save_changes(self):
        username = self.username_input.text()
        password = self.password_input.text()
        # Burada kullanıcı adı ve şifreyi kaydedebilirsiniz
        self.accept()

    def select_theme(self):
        color = QColorDialog.getColor()
        if color.isValid():
            # Tema rengini güncelle
            app.setStyleSheet(f"QMainWindow {{background-color: {color.name()};}}")

class ToDoListApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yapılacaklar Listesi")

        self.tasks = []  # Bu, görevleri veritabanına eklemeden önce geçici olarak tutacak
        self.init_ui()
        self.create_database()
        self.load_tasks_from_db()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Görevler tablosu
        self.task_table = QTableWidget(self)
        self.task_table.setColumnCount(4)
        self.task_table.setHorizontalHeaderLabels(["Görev", "Başlangıç Tarihi", "Bitiş Tarihi", "Detaylar"])
        self.task_table.setStyleSheet("background-color: #F9D5D3;")  # Görevlerin arka planı farklı renkte (tozpembe)
        layout.addWidget(self.task_table)

        # Görev Ekle Butonu
        self.add_task_button = QPushButton("Görev Ekle")
        self.add_task_button.setStyleSheet("""
            QPushButton {
                background-color: #D0B3D6;  /* Soft pastel mor */
                color: white;
                border-radius: 12px;
                padding: 15px;
                font-size: 18px;
                font-family: Arial, sans-serif;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #A582D0;  /* Canlı pastel mor */
            }
        """)
        self.add_task_button.clicked.connect(self.open_add_task_dialog)
        layout.addWidget(self.add_task_button)

        # Görev Sil Butonu
        self.delete_task_button = QPushButton("Görev Sil")
        self.delete_task_button.setStyleSheet("""
            QPushButton {
                background-color: #D0B3D6;  /* Soft pastel mor */
                color: white;
                border-radius: 12px;
                padding: 15px;
                font-size: 18px;
                font-family: Arial, sans-serif;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #A582D0;  /* Canlı pastel mor */
            }
        """)
        self.delete_task_button.clicked.connect(self.delete_task)
        layout.addWidget(self.delete_task_button)

        # Ayarlar Butonu
        self.settings_button = QPushButton("Ayarlar")
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: #D0B3D6;  /* Soft pastel mor */
                color: white;
                border-radius: 12px;
                padding: 15px;
                font-size: 18px;
                font-family: Arial, sans-serif;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #A582D0;  /* Canlı pastel mor */
            }
        """)
        self.settings_button.clicked.connect(self.open_settings_dialog)
        layout.addWidget(self.settings_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Pencerenin genel arka planını pastel pembe tonlarında ayarlama
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(253, 228, 236))  # Çok açık pastel pembe
        self.setPalette(palette)

    def open_add_task_dialog(self):
        add_task_dialog = AddTaskDialog(self)
        if add_task_dialog.exec_() == QDialog.Accepted:
            task = add_task_dialog.get_task()
            self.add_task_to_table(task)
            self.add_task_to_db(task)

    def add_task_to_table(self, task):
        row_position = self.task_table.rowCount()
        self.task_table.insertRow(row_position)
        self.task_table.setItem(row_position, 0, QTableWidgetItem(task.title))
        self.task_table.setItem(row_position, 1, QTableWidgetItem(task.start_date.toString("yyyy-MM-dd")))
        self.task_table.setItem(row_position, 2, QTableWidgetItem(task.end_date.toString("yyyy-MM-dd")))
        details_button = QPushButton("Detayları Gör")
        details_button.clicked.connect(lambda: self.show_task_details(task))
        self.task_table.setCellWidget(row_position, 3, details_button)

    def show_task_details(self, task):
        details_window = TaskDetailsWindow(task)
        details_window.exec_()

    def delete_task(self):
        selected_row = self.task_table.currentRow()
        if selected_row != -1:
            task_title = self.task_table.item(selected_row, 0).text()
            self.remove_task_from_db(task_title)
            self.task_table.removeRow(selected_row)

    def open_settings_dialog(self):
        settings_dialog = SettingsDialog()
        settings_dialog.exec_()

    def create_database(self):
        # Veritabanına bağlantı oluşturma
        self.conn = sqlite3.connect('tasks.db')
        self.cursor = self.conn.cursor()

        # Görevler tablosunu oluşturma (varsa tekrar oluşturmaz)
        self.cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            start_date TEXT,
            end_date TEXT
        )
        ''')
        self.conn.commit()

    def add_task_to_db(self, task):
        self.cursor.execute(''' 
        INSERT INTO tasks (title, description, start_date, end_date) 
        VALUES (?, ?, ?, ?)
        ''', (task.title, task.description, task.start_date.toString("yyyy-MM-dd"), task.end_date.toString("yyyy-MM-dd")))
        self.conn.commit()

    def remove_task_from_db(self, task_title):
        self.cursor.execute('DELETE FROM tasks WHERE title = ?', (task_title,))
        self.conn.commit()

    def load_tasks_from_db(self):
        self.cursor.execute('SELECT * FROM tasks')
        tasks = self.cursor.fetchall()

        for task in tasks:
            title, description, start_date, end_date = task[1], task[2], task[3], task[4]
            task_obj = Task(title, description, QDate.fromString(start_date, "yyyy-MM-dd"), QDate.fromString(end_date, "yyyy-MM-dd"))
            self.add_task_to_table(task_obj)

    def closeEvent(self, event):
        self.conn.close()

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super(AddTaskDialog, self).__init__(parent)
        self.setWindowTitle("Görev Ekle")
        self.setFixedSize(400, 300)

        layout = QFormLayout()

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Görev Başlığı")
        layout.addRow("Başlık:", self.title_input)

        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Görev Açıklaması")
        layout.addRow("Açıklama:", self.description_input)

        self.start_date_input = QDateEdit(self)
        self.start_date_input.setDate(QDate.currentDate())
        layout.addRow("Başlangıç Tarihi:", self.start_date_input)

        self.end_date_input = QDateEdit(self)
        self.end_date_input.setDate(QDate.currentDate())
        layout.addRow("Bitiş Tarihi:", self.end_date_input)
        self.save_button = QPushButton("Kaydet", self)
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def get_task(self):
        title = self.title_input.text()
        description = self.description_input.text()
        start_date = self.start_date_input.date()
        end_date = self.end_date_input.date()
        return Task(title, description, start_date, end_date)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        window = ToDoListApp()
        window.show()
        sys.exit(app.exec_())
