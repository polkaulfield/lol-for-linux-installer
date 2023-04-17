# lol-for-linux-installer

League of Legends unofficial installer for linux

This software is not affiliated with nor supported by Riot Games.

![Screenshot_20230415_205958](https://user-images.githubusercontent.com/40970965/232259098-0e51d868-cfb8-4312-aab4-6e84728c5f24.png)


## How to install it (Python version - Recommended)
- Check if you have all required [dependencies](#dependencies) installed first
- Download the latest release from the [Releases page](https://github.com/kassindornelles/lol-for-linux-bash-installer/releases)
- Extract the files
- Double-click 'launch-league-of-legends.py' and install the game or manage your already existent install.

### Python Script features:
- You can choose where to install the game and also the region you are going to play
- It installs wine-ge-lol with FSYNC/FUTEX2 support enabled by default for better CPU performance
- Installs the latest DXVK version to translate DirectX 9 and 11 to Vulkan for better performance

   Check if your GPU driver can run recent DXVK versions before opening a issue, [Check it here](https://github.com/doitsujin/dxvk/wiki/Driver-support)
   
- It creates a desktop file in the system menu (with icons for the game)
- Creates an uninstaller in case you want to nuke the game, after you rage quit a match that your teammates did everything they could to make you lose
- Users of hybrid graphics can choose at install time if they want to use the dGPU or not
- Update system for WINE builds, DXVK version selection and more

## How to install it (Bash version - Limited functionality, more like a backup
- Check if you have all required [dependencies](#dependencies) installed first
- Download the latest release from the [Releases page](https://github.com/kassindornelles/lol-for-linux-bash-installer/releases)
- Extract the files
- Run the `Install League of Legends (Bash).sh` script in a terminal/console:

   Open a console/terminal in the script main directory (where the files are)

   Type and run ```chmod +x ./'Install League of Legends (Bash).sh'``` first

   Type and run `./'Install League of Legends (Bash).sh'` to install the game


## <a name="dependencies"></a> Dependencies (install those packages system-wide first):
- `fuse` (AppImage)
- `winetricks`
- `wget` (Bash script)
- `kdialog` (Bash script)
- `tar`
- `python`, `python-requests` and `python-psutil` (Python script)

- `qt5-base` and `pyqt5` (Python script)
- WINE 32-64 bits and its [Dependency hell](https://www.gloriouseggroll.tv/how-to-get-out-of-wine-dependency-hell/)

## Remaining tasks and known problems:
- NVIDIA Hybrid Graphics users can't boot the game with the dedicated GPU

   Workaround for nvidia hybrid graphics: Copy the content of this file: https://github.com/kassindornelles/lol-for-linux-installer/raw/main/python_src/src/launch-script-nvidia-hybrid.py and replace the content of your "launch-script.py" file with it.
   
- Flatpak it

## Can i uninstall the game?
- You can with the Python script, as it will generate an `uninstall.py` file in the directory you installed the game.

- The bash script does not have a uninstaller script, but you can remove it manually by deleting the leagueoflegends desktop file from `/.local/share/applications` and deleting the game folder.

## Buy me a coffee

<a href="https://www.paypal.com/donate/?hosted_button_id=UMJWYGDH2RC7E"><img src="https://github.com/andreostrovsky/donate-with-paypal/blob/master/grey.svg" alt="Donate with PayPal" width="150" height="40"></a>

