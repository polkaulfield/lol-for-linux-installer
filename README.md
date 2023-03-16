# lol-for-linux-installer
Bash and Python scripts that installs league of legends automagically!

Warning: DON'T RUN THIS SCRIPT AS SUDO USER

## How to install it (Bash version)
- Download the latest release from the [Releases page](https://github.com/kassindornelles/lol-for-linux-bash-installer/releases)
- Extract the files
- Run the "leagueinstaller.sh" script in a terminal/console:

   Open a console/terminal in the script main directory (where the files are)
   
   Type `./leagueinstaller.sh` and press enter, might be necessary to run ```chmod +x ./leagueinstaller.sh``` first.

## How to install it (Python version - EXPERIMENTAL)
- Download the latest release from the [Releases page](https://github.com/kassindornelles/lol-for-linux-bash-installer/releases)
- Extract the files
- Run the "ui_installer.py" script in a terminal/console:

  Open a console/terminal in the script main directory (where the files are)
  
  Type `python ui_installer.py` and press enter.

## Dependencies, install those packages system-wide first:
- winetricks
- xdg-user-dirs
- wget
- wine (both 32-bit and 64-bit support)
- tar
- kdialog (for the Bash version of the script)
- qt5-base and pyqt5 (for the Python version of the script)
- And the rest of the dependency hell that comes with [WINE](https://www.gloriouseggroll.tv/how-to-get-out-of-wine-dependency-hell/)

## Remaining tasks:
- Flatpak it

## Buy me a coffee
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate/?hosted_button_id=9D3JQM8NAYS98)
