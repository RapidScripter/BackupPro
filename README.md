# BackupPro

BackupPro is a powerful and user-friendly backup tool designed to support both full and incremental backups. Built using PyQt5, BackupPro offers a simple and intuitive graphical interface for selecting source and backup folders, ensuring your data is safely stored with minimal effort.

## Features

- **Full and Incremental Backups**: BackupPro efficiently performs both full and incremental backups, saving time and storage space by only backing up new or modified files.
- **Easy-to-Use Interface**: A clean and straightforward GUI makes it easy to configure and perform backups.
- **Progress Monitoring**: A progress bar provides real-time feedback on the backup process.
- **Customizable Themes**: Leverage qt-material to apply modern material design themes to the application.
- **Error Handling and Notifications**: Informative error messages and notifications ensure the user is always aware of the backup status.

## Requirements

- Python 3.x
- PyQt5
- qt-material

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RapidScripter/BackupPro.git
   cd BackupPro

2. Install Required Packages
   ```bash
   pip install -r requirements.txt

## Usage

1. Run the Application
   ```bash
   python BackupPro.py

2. **Select Folders**: Use the "Browse..." buttons to select the source folder (the folder you want to back up) and the backup folder (the destination where the backup will be stored).

3. **Start the Backup**: Click the "Backup" button to initiate the backup process. The progress bar will update to show the backup progress. 

## Screenshots

![Alt text](/Screenshots/main_window.jpg?raw=true "Backup Tool")
