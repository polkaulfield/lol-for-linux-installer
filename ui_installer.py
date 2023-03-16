import sys
import os
import signal
import psutil
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
        self.cancelButton.clicked.connect(self.cancel_installation)
        self.install_button.setEnabled(False)
        self.cancelButton.hide()

    def select_folder_path(self):
        self.game_main_dir = QFileDialog.getExistingDirectory(self, 'Where do you want to install the game?')
        if self.game_main_dir:
            self.install_button.setEnabled(True)
        else:
            # Handle case where user pressed cancel
            print("User pressed cancel")

    def start_installation(self):
        self.selectFolder.hide()
        self.cancelButton.show()
        self.cancelButton.setEnabled(True)
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

    def cancel_installation(self):
        # Get the PID of the current process
        pid = os.getpid()

        # Get a list of all child processes
        children = psutil.Process(pid).children(recursive=True)

        # Terminate all child processes
        for child in children:
            child.send_signal(signal.SIGTERM)

        # Terminate the main application process
        os.kill(pid, signal.SIGTERM)

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
