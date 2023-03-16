import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import QThread, pyqtSignal, QObject, Qt
from subprocess import Popen
from queue import Queue
from PyQt5.QtGui import QIcon


class Installer(QMainWindow):
    def __init__(self):
        super(Installer, self).__init__()
        loadUi("installer.ui", self)  # load the UI from the .ui file
        self.setFixedSize(self.size())
        self.setWindowTitle('League of Legends installer')
        self.install_button.clicked.connect(self.start_installation)
        self.selectFolder.clicked.connect(self.select_folder_path)

    def select_folder_path(self):
        self.game_main_dir = QFileDialog.getExistingDirectory(self, 'Select Folder')

    def start_installation(self):
        self.selectFolder.hide()
        self.welcomelabel.setText("This may take a while based on your internet and system speed...")
        self.install_button.hide()  # hide the button
        self.adviselabel.setText("Installing, please be patient. \n This window will close itself when the install process is done \n Launch the game using the shortcut in the system menu")

        # Create a new thread to run the installation process
        self.thread = QThread()
        self.installer = LeagueInstaller(self.game_main_dir)
        self.installer.moveToThread(self.thread)
        self.installer.finished.connect(self.installation_finished)
        self.thread.started.connect(self.installer.run)
        self.thread.start()

    def installation_finished(self):
        self.welcomelabel.setText("Installation finishing, leaving installer...")
        self.adviselabel.hide()
        sys.exit(app.exec_())

class LeagueInstaller(QObject):
    finished = pyqtSignal()

    def __init__(self, game_main_dir):
        super().__init__()
        self.game_main_dir = game_main_dir  # store the game_main_dir variable as an instance attribute

    def run(self):
        # We run the 'leagueinstaller.py' script here
        import subprocess
        import os
        subprocess.call(['python', 'leagueinstaller.py', self.game_main_dir])

        self.finished.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    installer = Installer()
    installer.show()
    sys.exit(app.exec_())
