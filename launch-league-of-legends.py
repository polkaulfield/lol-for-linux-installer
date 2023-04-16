#!/usr/bin/env python3
import sys, os, signal, psutil, logging, json, urllib.request, shutil, tarfile, subprocess, time
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QComboBox, QCheckBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QThread, QObject, QUrl, pyqtSignal, QTimer
from PyQt5.QtGui import QDesktopServices
import leagueinstaller_code

class GuiLogHandler(QObject, logging.Handler):
    new_record = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)
        super(logging.Handler).__init__()
        formatter = Formatter('%(levelname)s: %(message)s', '%d/%m/%Y %H:%M:%S')
        self.setFormatter(formatter)

    def emit(self, record):
        msg = self.format(record)
        self.new_record.emit(msg) # <---- emit signal here

class Formatter(logging.Formatter):
    def formatException(self, ei):
        result = super(Formatter, self).formatException(ei)
        return result

    def format(self, record):
        s = super(Formatter, self).format(record)
        if record.exc_text:
            s = s.replace('\n', '')
        return s

class Installer(QMainWindow):
    def __init__(self):
        super(Installer, self).__init__()
        # Hacky workaround so the AppImage works
        try:
            loadUi("python_src/ui/installer.ui", self)
        except:
            loadUi("/usr/share/lolforlinux/ui/installer.ui", self)
        self.setFixedSize(self.size())
        self.setWindowTitle('League of Legends Manager')
        self.install_button.clicked.connect(self.installer_code)
        self.cancelButton.clicked.connect(self.cancel_installation)
        self.install_button.setEnabled(True)
        self.githubButton.clicked.connect(self.open_github)
        self.cancelButton.setEnabled(False)
        self.uninstallLeaguebutton.clicked.connect(self.uninstall_game)
        self.checkWineupdates.clicked.connect(self.update_wine_build)
        self.applyButton.setEnabled(False)
        self.applyButton.clicked.connect(self.applynewsettings)
        self.Usedriprime.stateChanged.connect(self.toggleapplybutton)
        self.Usenvidiahybrid.stateChanged.connect(self.toggleapplybutton)

        try:
            json_file_path = os.path.expanduser("~/.config/league_install_path.json")

            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)

            game_installed_folder = data["game_main_dir"]
            self.stackedWidget.setCurrentWidget(self.gamemanager)

            # Check NVIDIA HYBRID
            with open('env_vars.json', 'r') as f:
                env_vars = json.load(f)

            # Check if the environment variables exist in the file
            if all(key in env_vars for key in ['NV_PRIME_RENDER_OFFLOAD', '__GLX_VENDOR_LIBRARY_NAME', 'VK_ICD_FILENAMES', 'VK_LAYER_NV_optimus']):
                self.Usenvidiahybrid.setChecked(True)
            else:
                self.Usenvidiahybrid.setChecked(False)

            # Check DRI_PRIME
            with open('env_vars.json', 'r') as f:
                env_vars = json.load(f)

            # Check if the environment variables exist in the file
            if all(key in env_vars for key in ['DRI_PRIME']):
                self.Usedriprime.setChecked(True)
            else:
                self.Usedriprime.setChecked(False)

            # dxvk combobox
            # todo

        except FileNotFoundError:
            self.stackedWidget.setCurrentWidget(self.welcome)

        self.nextWelcome.clicked.connect(self.regionWidget)
        self.nextRegion.clicked.connect(self.optionsWidget)
        self.launchLeagueinstalled.clicked.connect(self.launchleague)

    def toggleapplybutton(self):
        self.applyButton.setEnabled(True)

    def applynewsettings(self):
        if self.Usedriprime.isChecked():
                # Load the environment variables from the JSON file
                with open('env_vars.json', 'r') as f:
                    env_vars = json.load(f)

                # Add the DRI_PRIME key to the dictionary if it doesn't already exist
                if 'DRI_PRIME' not in env_vars:
                    env_vars['DRI_PRIME'] = '1'

                # Write the updated dictionary back to the JSON file with indentation
                with open('env_vars.json', 'w') as f:
                    json.dump(env_vars, f, indent=4)
        else:
                # Load the environment variables from the JSON file
                with open('env_vars.json', 'r') as f:
                    env_vars = json.load(f)

                # Remove the DRI_PRIME key from the dictionary if it exists
                if 'DRI_PRIME' in env_vars:
                    del env_vars['DRI_PRIME']

                # Write the updated dictionary back to the JSON file with indentation
                with open('env_vars.json', 'w') as f:
                    json.dump(env_vars, f, indent=4)

        if self.Usenvidiahybrid.isChecked():
            # Load the environment variables from the JSON file
            with open('env_vars.json', 'r') as f:
                env_vars = json.load(f)

            # Define a dictionary of environment variables to add
            new_vars = {
                'NV_PRIME_RENDER_OFFLOAD': '1',
                '__GLX_VENDOR_LIBRARY_NAME': 'nvidia',
                'VK_ICD_FILENAMES': '/usr/share/vulkan/icd.d/nvidia_icd.json',
                'VK_LAYER_NV_optimus': 'NVIDIA_only'
            }

            # Add the new variables to the dictionary if they don't already exist
            for var_name, var_value in new_vars.items():
                if var_name not in env_vars:
                    env_vars[var_name] = var_value

            # Write the updated dictionary back to the JSON file with indentation
            with open('env_vars.json', 'w') as f:
                json.dump(env_vars, f, indent=4)
        else:
            # Load the environment variables from the JSON file
            with open('env_vars.json', 'r') as f:
                env_vars = json.load(f)

            # Define a list of environment variables to remove
            vars_to_remove = [
                'NV_PRIME_RENDER_OFFLOAD',
                '__GLX_VENDOR_LIBRARY_NAME',
                'VK_ICD_FILENAMES',
                'VK_LAYER_NV_optimus'
            ]

            # Remove the variables from the dictionary if they exist
            for var_name in vars_to_remove:
                if var_name in env_vars:
                    del env_vars[var_name]

            # Write the updated dictionary back to the JSON file with indentation
            with open('env_vars.json', 'w') as f:
                json.dump(env_vars, f, indent=4)

    def launchleague(self):
        json_file_path = os.path.expanduser("~/.config/league_install_path.json")

        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        game_installed_folder = data["game_main_dir"]
        self.stackedWidget.setCurrentWidget(self.gamemanager)
        os.chdir(game_installed_folder)
        process = subprocess.Popen(['python3', 'launch-script.py'])
        self.hide()

        while True:
            retcode = process.poll()
            if retcode is not None:
                self.show()
                break
            time.sleep(0.5)

    def regionWidget(self):
        self.stackedWidget.setCurrentWidget(self.region)

    def optionsWidget(self):
        self.stackedWidget.setCurrentWidget(self.options)

    def open_github(self):
        url = "https://github.com/kassindornelles/lol-for-linux-installer/issues"
        QDesktopServices.openUrl(QUrl(url))

    def update_wine_build(self):
        self.checkWineupdates.setEnabled(False)
        self.checkWineupdates.setText("Updating...")
        self.uninstallLeaguebutton.setEnabled(False)
        self.launchLeagueinstalled.setEnabled(False)
        json_file_path = os.path.expanduser("~/.config/league_install_path.json")

        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        game_installed_folder = data["game_main_dir"]
        json_url = "https://raw.githubusercontent.com/kassindornelles/lol-for-linux-installer/main/wine_build.json"
        filename = "wine_build.json"
        os.chdir(game_installed_folder)
        urllib.request.urlretrieve(json_url, filename)

        with open(filename, "r") as f:
            data = json.load(f)

        with open("buildversion.json", "r") as f:
            existing_data = json.load(f)

        print("Value of wine_build.json:", data["current_build_name"])
        print("Value of buildversion.json:", existing_data["current_build_name"])

        if data["current_build_name"].split("/")[-1] > existing_data["current_build_name"].split("/")[-1]:
            print("Update needed")

            build_url = data["current_build_name"]
            build_filename = build_url.split("/")[-1]
            urllib.request.urlretrieve(build_url, build_filename)

            temp_dir = "tmp"
            os.makedirs(temp_dir, exist_ok=True)
            with tarfile.open(build_filename, "r:xz") as tar:
                tar.extractall(path=temp_dir)

            wine_build_dir = "wine/wine-build"
            if os.path.exists(wine_build_dir):
                shutil.rmtree(wine_build_dir)

            extract_path = os.path.join(temp_dir, os.listdir(temp_dir)[0])
            shutil.move(extract_path, wine_build_dir)

            existing_data["current_build_name"] = data["current_build_name"]
            with open("buildversion.json", "w") as f:
                json.dump(existing_data, f)

            os.remove(filename)
            if os.path.exists(build_filename):
                os.remove(build_filename)
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

            self.checkWineupdates.setEnabled(True)
            self.checkWineupdates.setText("Game is up-to-date!")
            self.uninstallLeaguebutton.setEnabled(True)
            self.launchLeagueinstalled.setEnabled(True)

        else:
            print("No need to update")
            self.checkWineupdates.setEnabled(False)
            self.checkWineupdates.setText("Game is up-to-date!")
            self.uninstallLeaguebutton.setEnabled(True)
            self.launchLeagueinstalled.setEnabled(True)


    def uninstall_game(self):
        home_dir = os.path.expanduser("~")
        user_local_share = os.path.join(home_dir, ".local/share")
        desktop_file_path = os.path.join(os.path.expanduser("~"), ".local", "share", "applications", "LeagueLauncherPython.desktop")
        user_config_folder= os.path.join(home_dir, ".config")
        json_file_path = os.path.join(user_config_folder, "league_install_path.json")

        try:
            # Read the JSON file and get the game_main_dir value
            with open(json_file_path, "r") as infile:
                data = json.load(infile)
                game_main_dir = data["game_main_dir"]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # Handle the exception by printing an error message
            print(f"Failed to read JSON file: {e}")

        try:
            shutil.rmtree(game_main_dir)
        except FileNotFoundError:
            print(f"Directory {self.game_installed_folder} does not exist")

        try:
            os.remove(desktop_file_path)
        except FileNotFoundError:
            print(f"File {desktop_file_path} does not exist")

        try:
            os.remove(json_file_path)
        except FileNotFoundError:
            print(f"File {json_file_path} does not exist")

        QApplication.quit()

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

    def addPlainText(self, text: str):
        self.textOuput.appendPlainText(text)

    def setup_logger(self):

        # Send info logs to textOutput
        handler = GuiLogHandler(self)
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.INFO)
        handler.new_record.connect(self.textOutput.append)

        # Send debug logs to stdout
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(Formatter('%(levelname)s: %(message)s\n', '%d/%m/%Y %H:%M:%S'))
        stream_handler.setLevel(logging.DEBUG)
        logging.getLogger().addHandler(stream_handler)

    def installer_code(self):
        self.game_main_dir = QFileDialog.getExistingDirectory(self, 'Where do you want to install the game?')
        while self.game_main_dir and os.path.abspath(self.game_main_dir) == os.path.expanduser("~"):
            # If the user selected their home directory, display an error message
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Cannot install the game directly in the home directory.")
            msg_box.setInformativeText("Please create a folder in your home directory instead so we can use it")
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg_box.setDefaultButton(QMessageBox.Ok)
            if msg_box.exec_() == QMessageBox.Ok:
                # If the user clicks "Ok", allow them to select a different directory
                self.game_main_dir = QFileDialog.getExistingDirectory(self, 'Where do you want to install the game?')
            else:
                # If the user clicks "Cancel", exit the loop and do not set the directory
                self.game_main_dir = None

        # Check if the selected directory is inside the user's home directory
        if not os.path.abspath(self.game_main_dir).startswith(os.path.expanduser("~")):
            # If not, display an error message and prompt the user to select a different directory
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Invalid directory selected.")
            msg_box.setInformativeText("Please select a directory within your home directory.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setDefaultButton(QMessageBox.Ok)
            msg_box.exec_()
            self.game_main_dir = QFileDialog.getExistingDirectory(self, 'Where do you want to install the game?')

        if self.game_main_dir:
            self.cancelButton.show()
            self.cancelButton.setEnabled(True)
            self.checkShortcut.setEnabled(False)
            self.welcomelabel.setText("We are installing the game for you...")
            self.install_button.setEnabled(False)
            self.languageComboBox.setEnabled(False)
            self.regionLabel.setEnabled(False)
            self.checkPrime.setEnabled(False)
            self.stackedWidget.setCurrentWidget(self.installing)

            # Get the game download link and apply region based on text from .ui file
            region_map = {
                "BR (BR1) - Brazil": "br",
                "LAN (LA1) - Latin America North": "la1",
                "LAS (LA2) - Latin America South": "la2",
                "NA (NA1) - North America": "na",
                "OCE (OCE/OC1) - Oceania": "oc1",
                "RU (RU1) - Russia": "ru",
                "EUW (EUW1) - Europe West": "euw",
                "EUNE (EUN1) - Europe Nordic & East": "eune",
                "TR (TR1) - Turkey": "tr",
                "JP (JP1) - Japan": "jp",
                "KR (KR) - Republic of Korea": "kr",
            }

            selected_lang = self.languageComboBox.currentText()
            game_link = "https://lol.secure.dyn.riotcdn.net/channels/public/x/installer/current/live.{}.exe"
            region = region_map.get(selected_lang, "na")
            game_region_link = game_link.format(region)

            self.setup_logger()
            scrollbar = self.textOutput.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

            if self.checkPrime.isChecked():
                # Load the environment variables from the JSON file
                with open('env_vars.json', 'r') as f:
                    env_vars = json.load(f)

                # Add the DRI_PRIME key to the dictionary if it doesn't already exist
                if 'DRI_PRIME' not in env_vars:
                    env_vars['DRI_PRIME'] = '1'

                # Write the updated dictionary back to the JSON file with indentation
                with open('env_vars.json', 'w') as f:
                    json.dump(env_vars, f, indent=4)
            else:
                # Load the environment variables from the JSON file
                with open('env_vars.json', 'r') as f:
                    env_vars = json.load(f)

                # Remove the DRI_PRIME key from the dictionary if it exists
                if 'DRI_PRIME' in env_vars:
                    del env_vars['DRI_PRIME']

                # Write the updated dictionary back to the JSON file with indentation
                with open('env_vars.json', 'w') as f:
                    json.dump(env_vars, f, indent=4)


            self.thread = QThread()
            self.worker = Worker(self.game_main_dir, game_region_link, self.checkShortcut.isChecked())
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.thread.finished.connect(self.finish_installation)
            self.thread.start()
            self.thread.quit()
        else:
            # Handle case where user pressed cancel
            print("User pressed cancel")

    def finish_installation(self):

        QApplication.quit()


class Worker(QObject):
    def __init__(self, game_main_dir, game_region_link, create_shortcut):
        super().__init__()
        self.game_main_dir = game_main_dir
        self.game_region_link = game_region_link
        self.create_shortcut = create_shortcut

    def run(self):
        leagueinstaller_code.league_install_code(self.game_main_dir, self.game_region_link, self.create_shortcut)
        QApplication.quit()

class QTextEditLogger(logging.Handler, QObject):
    appendPlainText = pyqtSignal(str)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    if os.getuid() == 0:
        msg_box = QMessageBox()
        msg_box.setText("Don't run this as sudo user")
        msg_box.exec_()
        sys.exit(1)

    installer = Installer()
    installer.show()
    sys.exit(app.exec_())