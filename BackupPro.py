import os
import time
import zipfile
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton, QMessageBox,
                             QVBoxLayout, QWidget, QFileDialog, QProgressBar)
from qt_material import apply_stylesheet
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon
import threading

class BackupSignals(QObject):
    progress_update = pyqtSignal(int)
    backup_complete = pyqtSignal()

class BackupWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.source_folder = ""
        self.backup_folder = ""
        self.last_backup_time = 0
        self.signals = BackupSignals()
        self.signals.progress_update.connect(self.update_progress_bar)
        self.signals.backup_complete.connect(self.backup_complete)
        self.init_ui()

    def init_ui(self):
        logo_icon = QIcon('icon.ico')
        title_label = QLabel("Full & Incremental Backup Tool")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20pt; font-weight: bold;")

        source_label = QLabel("Source Folder:")
        source_label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        backup_label = QLabel("Backup Folder:")
        backup_label.setStyleSheet("font-size: 16pt; font-weight: bold;")

        self.source_edit = QLineEdit()
        self.backup_edit = QLineEdit()

        source_browse_button = QPushButton("Browse...")
        backup_browse_button = QPushButton("Browse...")

        source_browse_button.clicked.connect(self.select_source_folder)
        backup_browse_button.clicked.connect(self.select_backup_folder)

        backup_button = QPushButton("Backup")
        backup_button.setObjectName("backupButton")
        backup_button.setCursor(Qt.PointingHandCursor)
        backup_button.setStyleSheet("""
            QPushButton#backupButton:hover {
                background-color: #4c4c4c;
                color: white;
            }
        """)
        backup_button.clicked.connect(self.backup)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addSpacing(20)
        layout.addWidget(source_label)
        layout.addWidget(self.source_edit)
        layout.addWidget(source_browse_button)
        layout.addSpacing(10)
        layout.addWidget(backup_label)
        layout.addWidget(self.backup_edit)
        layout.addWidget(backup_browse_button)
        layout.addSpacing(30)
        layout.addWidget(self.progress_bar)
        layout.addWidget(backup_button)
        layout.addSpacing(10)

        self.setLayout(layout)
        self.setWindowIcon(logo_icon)
        self.setWindowTitle("BackupPro")
        self.setFixedSize(700, 450)

        apply_stylesheet(app, theme='dark_cyan.xml')
        self.show()

    def select_source_folder(self):
        self.source_folder = QFileDialog.getExistingDirectory(
            self, "Select Source Folder", "/")
        self.source_edit.setText(self.source_folder)

    def select_backup_folder(self):
        self.backup_folder = QFileDialog.getExistingDirectory(
            self, "Select Backup Folder", "/")
        self.backup_edit.setText(self.backup_folder)

    def load_last_backup_time(self):
        if not self.backup_folder:
            return
        backup_path = os.path.join(self.backup_folder, "last_backup_time.txt")
        if os.path.exists(backup_path):
            with open(backup_path, "r") as backup_file:
                timestamp_str = backup_file.read().strip()
                self.last_backup_time = time.mktime(time.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S"))

    def save_last_backup_time(self):
        if not self.backup_folder:
            return
        backup_path = os.path.join(self.backup_folder, "last_backup_time.txt")
        with open(backup_path, "w") as backup_file:
            backup_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.last_backup_time)))

    def find_files_to_backup(self):
        files_to_backup = []
        total_size = 0
        for foldername, subfolders, filenames in os.walk(self.source_folder):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                mod_time = os.path.getmtime(file_path)
                if mod_time > self.last_backup_time:
                    files_to_backup.append(file_path)
                    total_size += os.path.getsize(file_path)
        return files_to_backup, total_size

    def create_backup_zip(self, files_to_backup, total_size):
        backup_filename = time.strftime("%Y-%m-%d_%H-%M-%S") + ".zip"
        backup_path = os.path.join(self.backup_folder, backup_filename)
        with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as backup_zip:
            processed_size = 0
            for file_path in files_to_backup:
                backup_zip.write(file_path, arcname=os.path.relpath(file_path, self.source_folder))
                processed_size += os.path.getsize(file_path)
                progress = int(processed_size / total_size * 100)
                self.signals.progress_update.emit(progress)
        return backup_path

    def backup_thread(self):
        if not self.source_folder or not self.backup_folder:
            self.show_error("Please select both source and backup folders.")
            return

        self.load_last_backup_time()
        files_to_backup, total_size = self.find_files_to_backup()
        if not files_to_backup:
            self.show_error("No new or modified files to backup.")
            return

        self.create_backup_zip(files_to_backup, total_size)
        self.last_backup_time = time.time()
        self.save_last_backup_time()
        self.signals.backup_complete.emit()

    def update_progress_bar(self, progress):
        self.progress_bar.setValue(progress)

    def backup_complete(self):
        QMessageBox.information(self, "Backup Successful", "Your backup was successful!")
        self.source_edit.clear()
        self.backup_edit.clear()
        self.source_folder = ""
        self.backup_folder = ""
        self.progress_bar.setValue(0)

    def backup(self):
        backup_thread = threading.Thread(target=self.backup_thread)
        backup_thread.start()

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

if __name__ == "__main__":
    app = QApplication([])
    backup_widget = BackupWidget()
    app.exec_()
