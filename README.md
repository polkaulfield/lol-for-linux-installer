# lol-for-linux-installer
Bash and Python scripts that installs league of legends automagically!

Warning: DON'T RUN THIS SCRIPT AS SUDO USER

## How to install it (Python version - Recommended)
- Download the latest release from the [Releases page](https://github.com/kassindornelles/lol-for-linux-bash-installer/releases)
- Extract the files
- Run the "ui_installer.py" script in a terminal/console:

  Open a console/terminal in the script main directory (where the files are)

  Type `python 'Install League of Legends (Python).py'` and press enter.
  
- Alternatively you can go to the 'Install League of Legends (Python).py' file properties, set it as executable and then double-click to open it

## How to install it (Bash version - Simpler and safer version)
- Download the latest release from the [Releases page](https://github.com/kassindornelles/lol-for-linux-bash-installer/releases)
- Extract the files
- Run the "Install League of Legends (Bash).sh" script in a terminal/console:

   Open a console/terminal in the script main directory (where the files are)

   Type and run ```chmod +x ./'Install League of Legends (Bash).sh'``` first
   
   Type and run `./'Install League of Legends (Bash).sh'` to install the game


## Dependencies, install those packages system-wide first:
- winetricks
- wget (Bash script)
- kdialog (Bash script)
- tar
- python and python-requests (Python script)
- qt5-base and pyqt5 (Python script)
- WINE 32-64 bits and its [Dependency hell](https://www.gloriouseggroll.tv/how-to-get-out-of-wine-dependency-hell/)

## Remaining tasks:
- Flatpak it

## Can i uninstall the game?
- You can with the Python script, it will generate a uninstall.py file in the directory you installed the game.

- The bash script does not have a uninstaller script, but you can remove it manually by deleting the leagueoflegends desktop file from /.local/share/applications and also deleting the game folder.

## Buy me a coffee
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate/?hosted_button_id=9D3JQM8NAYS98)
