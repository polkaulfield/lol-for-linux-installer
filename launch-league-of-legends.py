#!/usr/bin/env python3
import sys, os, signal, psutil, logging, json, urllib.request, shutil, tarfile, subprocess, time, requests, tempfile
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
        self.Checkupdates.clicked.connect(self.checkforupdates)

        self.tabWidget.setCurrentIndex(0)

        json_file_path = os.path.expanduser("~/.config/league_install_path.json")
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        game_installed_folder = data["game_main_dir"]
        os.chdir(game_installed_folder)

        with open('app_settings.json', 'r') as f:
            app_settings = json.load(f)

        current_version = app_settings['Version']
        self.setWindowTitle('League of Legends Manager ' + current_version)

        # Get the current display
        current_display = os.environ.get('DISPLAY')

        # Get the current desktop resolution for the current display using xrandr
        resolutions_output = subprocess.check_output(['xrandr', '-q', '-d', current_display]).decode('utf-8')
        current_resolution = ""
        for line in resolutions_output.splitlines():
            if '*' in line:
                # Extract the resolution from the line
                current_resolution = line.split()[0]

        # Check if the current resolution is already in the combobox
        if current_resolution not in ['1920x1080', '1280x720', '800x450']:
            # Add the current resolution to the top of the combobox
            self.resolutioncombobox.insertItem(0, current_resolution)

        try:
            json_file_path = os.path.expanduser("~/.config/league_install_path.json")

            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)

            game_installed_folder = data["game_main_dir"]
            self.stackedWidget.setCurrentWidget(self.gamemanager)
            os.chdir(game_installed_folder)
            with open('env_vars.json', 'r') as f:
                env_vars = json.load(f)

            if all(key in env_vars for key in ['NV_PRIME_RENDER_OFFLOAD', '__GLX_VENDOR_LIBRARY_NAME', 'VK_ICD_FILENAMES', 'VK_LAYER_NV_optimus']):
                self.Usenvidiahybrid.setChecked(True)
            else:
                self.Usenvidiahybrid.setChecked(False)

            with open('env_vars.json', 'r') as f:
                env_vars = json.load(f)

            if all(key in env_vars for key in ['DRI_PRIME']):
                self.Usedriprime.setChecked(True)
            else:
                self.Usedriprime.setChecked(False)

            if all(key in env_vars for key in ['MANGOHUD']):
                self.Usemangohud.setChecked(True)
            else:
                self.Usemangohud.setChecked(False)

        except FileNotFoundError:
            self.stackedWidget.setCurrentWidget(self.welcome)

        try:
            json_file_path = os.path.expanduser("~/.config/league_install_path.json")
            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)
            game_installed_folder = data["game_main_dir"]
            self.stackedWidget.setCurrentWidget(self.gamemanager)
            os.chdir(game_installed_folder)

            with open('app_settings.json', 'r') as f:
                app_settings = json.load(f)

            if app_settings['FSR'] == '1':
                self.Usefsrcheckbox.setChecked(True)
            else:
                self.Usefsrcheckbox.setChecked(False)
            if app_settings['Gamescope'] == "1":
                self.Usegamescope.setChecked(True)
            else:
                self.Usegamescope.setChecked(False)

            resolution = app_settings['Resolution']
            if resolution not in [self.resolutioncombobox.itemText(i) for i in range(self.resolutioncombobox.count())]:
                self.resolutioncombobox.addItem(resolution)
            self.resolutioncombobox.setCurrentText(resolution)

        except FileNotFoundError:
            self.stackedWidget.setCurrentWidget(self.welcome)

        self.Usedriprime.stateChanged.connect(self.toggleapplybutton)
        self.Usenvidiahybrid.stateChanged.connect(self.toggleapplybutton)
        self.Usemangohud.stateChanged.connect(self.toggleapplybutton)
        self.rendererCombobox.currentIndexChanged.connect(self.toggleapplybutton)
        self.nextWelcome.clicked.connect(self.regionWidget)
        self.nextRegion.clicked.connect(self.optionsWidget)
        self.launchLeagueinstalled.clicked.connect(self.launchleague)
        self.Usefsrcheckbox.clicked.connect(self.toggleapplybutton)
        self.Usegamescope.clicked.connect(self.toggleapplybutton)
        self.resolutioncombobox.currentIndexChanged.connect(self.toggleapplybutton)

    def checkforupdates(self):
        json_file_path = os.path.expanduser("~/.config/league_install_path.json")
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        game_installed_folder = data["game_main_dir"]
        os.chdir(game_installed_folder)

        with open('app_settings.json', 'r') as f:
            app_settings = json.load(f)

        current_version = app_settings['Version']
        current_version = current_version[1:]
        current_version_parts = current_version.split('.')
        current_version_major = int(current_version_parts[0])
        current_version_minor = int(current_version_parts[1])
        current_version_patch = int(current_version_parts[2])
        response = requests.get('https://api.github.com/repos/kassindornelles/lol-for-linux-installer/releases/latest')
        latest_version = response.json()['tag_name']
        latest_version = latest_version[1:]
        latest_version_parts = latest_version.split('.')
        latest_version_major = int(latest_version_parts[0])
        latest_version_minor = int(latest_version_parts[1])
        latest_version_patch = int(latest_version_parts[2])

        if latest_version_major > current_version_major:
            install_update(game_installed_folder, latest_version)
        elif latest_version_major == current_version_major and latest_version_minor > current_version_minor:
            install_update(game_installed_folder, latest_version)
        elif latest_version_major == current_version_major and latest_version_minor == current_version_minor and latest_version_patch > current_version_patch:
            install_update(game_installed_folder, latest_version)
        else:
            print("Up-to-date!")

    def install_update(self, game_installed_folder, latest_version):
        url = "https://github.com/kassindornelles/lol-for-linux-installer/archive/refs/tags/{}.tar.gz".format(latest_version)
        response = requests.get(url)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(response.content)

            with tarfile.open(temp_file.name, "r:gz") as archive:
                for member in archive.getmembers():
                    if member.name.endswith("lol-for-linux-installer.tar.gz"):
                        archive.extract(member, game_installed_folder)

            os.remove(temp_file.name)

            print("Update successful!")
        else:
            print("Error downloading latest release from GitHub")

    def toggleapplybutton(self):
        self.applyButton.setEnabled(True)

    def applynewsettings(self):
        json_file_path = os.path.expanduser("~/.config/league_install_path.json")
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        game_installed_folder = data["game_main_dir"]
        os.chdir(game_installed_folder)
        current_renderer = self.rendererCombobox.currentText()

        if current_renderer == 'DXVK 2.1':

            # 64 bit dlls
            dst_path = os.path.join(game_installed_folder, 'wine', 'prefix', 'drive_c', 'windows', 'system32')
            url = 'https://github.com/doitsujin/dxvk/releases/download/v2.1/dxvk-2.1.tar.gz'
            filename = os.path.basename(url)
            urllib.request.urlretrieve(url, filename)

            with tarfile.open(filename, 'r:gz') as tar:
                    tar.extractall('dxvk-tmp')

            src_path = os.path.join('dxvk-tmp', 'dxvk-2.1', 'x64')
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
            for file_name in os.listdir(src_path):
                if file_name.endswith('.dll') or file_name.endswith('.so'):
                    src_file = os.path.join(src_path, file_name)
                    dst_file = os.path.join(dst_path, file_name)
                    shutil.copy2(src_file, dst_file)

            # 32 bit dlls
            dst_path32 = os.path.join(game_installed_folder, 'wine', 'prefix', 'drive_c', 'windows', 'syswow64')

            src_path32 = os.path.join('dxvk-tmp', 'dxvk-2.1', 'x32')
            if not os.path.exists(dst_path32):
                os.makedirs(dst_path32)
            for file_name in os.listdir(src_path32):
                if file_name.endswith('.dll') or file_name.endswith('.so'):
                    src_file32 = os.path.join(src_path32, file_name)
                    dst_file32 = os.path.join(dst_path32, file_name)
                    shutil.copy2(src_file32, dst_file32)

            os.remove(filename)
            shutil.rmtree('dxvk-tmp')
            self.rendererCombobox.setEnabled(False)

        elif current_renderer == 'DXVK 1.10.3':

            # 64 bit dlls
            dst_path = os.path.join(game_installed_folder, 'wine', 'prefix', 'drive_c', 'windows', 'system32')
            url = 'https://github.com/doitsujin/dxvk/releases/download/v1.10.3/dxvk-1.10.3.tar.gz'
            filename = os.path.basename(url)
            urllib.request.urlretrieve(url, filename)

            with tarfile.open(filename, 'r:gz') as tar:
                    tar.extractall('dxvk-tmp')

            src_path = os.path.join('dxvk-tmp', 'dxvk-1.10.3', 'x64')
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
            for file_name in os.listdir(src_path):
                if file_name.endswith('.dll') or file_name.endswith('.so'):
                    src_file = os.path.join(src_path, file_name)
                    dst_file = os.path.join(dst_path, file_name)
                    shutil.copy2(src_file, dst_file)

            # 32 bit dlls
            dst_path32 = os.path.join(game_installed_folder, 'wine', 'prefix', 'drive_c', 'windows', 'syswow64')

            src_path32 = os.path.join('dxvk-tmp', 'dxvk-1.10.3', 'x32')
            if not os.path.exists(dst_path32):
                os.makedirs(dst_path32)
            for file_name in os.listdir(src_path32):
                if file_name.endswith('.dll') or file_name.endswith('.so'):
                    src_file32 = os.path.join(src_path32, file_name)
                    dst_file32 = os.path.join(dst_path32, file_name)
                    shutil.copy2(src_file32, dst_file32)

            os.remove(filename)
            shutil.rmtree('dxvk-tmp')
            self.rendererCombobox.setEnabled(False)

        if self.Usedriprime.isChecked():
                with open('env_vars.json', 'r') as f:
                    env_vars = json.load(f)

                if 'DRI_PRIME' not in env_vars:
                    env_vars['DRI_PRIME'] = '1'

                with open('env_vars.json', 'w') as f:
                    json.dump(env_vars, f, indent=4)
        else:
                with open('env_vars.json', 'r') as f:
                    env_vars = json.load(f)

                if 'DRI_PRIME' in env_vars:
                    del env_vars['DRI_PRIME']

                with open('env_vars.json', 'w') as f:
                    json.dump(env_vars, f, indent=4)

        if self.Usenvidiahybrid.isChecked():
            with open('env_vars.json', 'r') as f:
                env_vars = json.load(f)

            new_vars = {
                'NV_PRIME_RENDER_OFFLOAD': '1',
                '__GLX_VENDOR_LIBRARY_NAME': 'nvidia',
                'VK_ICD_FILENAMES': '/usr/share/vulkan/icd.d/nvidia_icd.json',
                'VK_LAYER_NV_optimus': 'NVIDIA_only'
            }

            for var_name, var_value in new_vars.items():
                if var_name not in env_vars:
                    env_vars[var_name] = var_value

            with open('env_vars.json', 'w') as f:
                json.dump(env_vars, f, indent=4)
        else:
            with open('env_vars.json', 'r') as f:
                env_vars = json.load(f)

            vars_to_remove = [
                'NV_PRIME_RENDER_OFFLOAD',
                '__GLX_VENDOR_LIBRARY_NAME',
                'VK_ICD_FILENAMES',
                'VK_LAYER_NV_optimus'
            ]

            for var_name in vars_to_remove:
                if var_name in env_vars:
                    del env_vars[var_name]

            with open('env_vars.json', 'w') as f:
                json.dump(env_vars, f, indent=4)


        if self.Usemangohud.isChecked():
            with open('env_vars.json', 'r') as f:
                env_vars = json.load(f)

            if 'MANGOHUD' not in env_vars:
                env_vars['MANGOHUD'] = '1'

            with open('env_vars.json', 'w') as f:
                json.dump(env_vars, f, indent=4)
        else:
            with open('env_vars.json', 'r') as f:
                env_vars = json.load(f)

            if 'MANGOHUD' in env_vars:
                del env_vars['MANGOHUD']

            with open('env_vars.json', 'w') as f:
                json.dump(env_vars, f, indent=4)

        if self.Usegamescope.isChecked():
            os.chdir(game_installed_folder)
            with open('app_settings.json', 'r') as f:
                app_settings = json.load(f)

            app_settings['Gamescope'] = '1'
            with open('app_settings.json', 'w') as f:
                json.dump(app_settings, f, indent=4)
        else:
            os.chdir(game_installed_folder)
            with open('app_settings.json', 'r') as f:
                app_settings = json.load(f)
            app_settings['Gamescope'] = '0'
            with open('app_settings.json', 'w') as f:
                json.dump(app_settings, f, indent=4)

        if self.Usefsrcheckbox.isChecked():
            os.chdir(game_installed_folder)
            with open('app_settings.json', 'r') as f:
                app_settings = json.load(f)

            app_settings['FSR'] = '1'
            with open('app_settings.json', 'w') as f:
                json.dump(app_settings, f, indent=4)
        else:
            os.chdir(game_installed_folder)
            with open('app_settings.json', 'r') as f:
                app_settings = json.load(f)
            app_settings['FSR'] = '0'
            with open('app_settings.json', 'w') as f:
                json.dump(app_settings, f, indent=4)

        os.chdir(game_installed_folder)
        with open('app_settings.json', 'r') as f:
            app_settings = json.load(f)

        app_settings['Resolution'] = self.resolutioncombobox.currentText()
        with open('app_settings.json', 'w') as f:
            json.dump(app_settings, f, indent=4)

        self.applyButton.setEnabled(False)

    def launchleague(self):
        self.launchLeagueinstalled.setEnabled(False)
        self.uninstallLeaguebutton.setEnabled(False)
        json_file_path = os.path.expanduser("~/.config/league_install_path.json")

        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        game_installed_folder = data["game_main_dir"]
        self.stackedWidget.setCurrentWidget(self.gamemanager)
        os.chdir(game_installed_folder)

        if self.Usegamescope.isChecked():
            process = subprocess.Popen(['gamescope', '-b', 'python3', 'launch-script.py'])
        else:
            process = subprocess.Popen(['python3', 'launch-script.py'])
        self.hide()
        while True:
            retcode = process.poll()
            if retcode is not None:
                self.show()
                self.launchLeagueinstalled.setEnabled(True)
                self.uninstallLeaguebutton.setEnabled(True)
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
            self.checkWineupdates.setText("Update completed!")
            self.uninstallLeaguebutton.setEnabled(True)
            self.launchLeagueinstalled.setEnabled(True)

        else:
            print("No need to update")
            self.checkWineupdates.setEnabled(False)
            self.checkWineupdates.setText("Game was up-to-date!")
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

        # Create the "league-of-legends" directory at the selected location
        self.game_main_dir = os.path.join(self.game_main_dir, "league-of-legends")
        os.makedirs(self.game_main_dir)

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


            if self.Checknvidiahybrid.isChecked():
                with open('env_vars.json', 'r') as f:
                    env_vars = json.load(f)

                new_vars = {
                    'NV_PRIME_RENDER_OFFLOAD': '1',
                    '__GLX_VENDOR_LIBRARY_NAME': 'nvidia',
                    'VK_ICD_FILENAMES': '/usr/share/vulkan/icd.d/nvidia_icd.json',
                    'VK_LAYER_NV_optimus': 'NVIDIA_only'
                }

                for var_name, var_value in new_vars.items():
                    if var_name not in env_vars:
                        env_vars[var_name] = var_value

                with open('env_vars.json', 'w') as f:
                    json.dump(env_vars, f, indent=4)
            else:
                with open('env_vars.json', 'r') as f:
                    env_vars = json.load(f)

                vars_to_remove = [
                    'NV_PRIME_RENDER_OFFLOAD',
                    '__GLX_VENDOR_LIBRARY_NAME',
                    'VK_ICD_FILENAMES',
                    'VK_LAYER_NV_optimus'
                ]

                for var_name in vars_to_remove:
                    if var_name in env_vars:
                        del env_vars[var_name]

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

        self.stackedWidget.setCurrentWidget(self.gamemanager)
        os.chdir(game_installed_folder)


class Worker(QObject):
    def __init__(self, game_main_dir, game_region_link, create_shortcut):
        super().__init__()
        self.game_main_dir = game_main_dir
        self.game_region_link = game_region_link
        self.create_shortcut = create_shortcut

    def run(self):
        leagueinstaller_code.league_install_code(self.game_main_dir, self.game_region_link, self.create_shortcut)
        self.stackedWidget.setCurrentWidget(self.gamemanager)
        os.chdir(game_installed_folder)

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
