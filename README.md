# lol-for-linux-installer




WARNING: THIS IS A FORK USING AN EXPERIMENTAL BUILD OF PROTON AND DEBUG FLAGS TO GET THE GAME RUNNING AT LEAST


League of Legends unofficial installer for linux

This software is not affiliated with nor supported by Riot Games.

![Screenshot_20230402_085233](https://user-images.githubusercontent.com/40970965/229351096-e30b9efe-fa78-4bb7-980d-a23496cf8b09.png)

## How to install it (Python version - Recommended)
- Check if you have all required [dependencies](#dependencies) installed first
- Download the latest release from the [Releases page](https://github.com/kassindornelles/lol-for-linux-bash-installer/releases)
- Extract the files
- Double-click 'Install League of Legends (Python).py' and install the game.

### Python Script features:
- You can choose where to install the game and also the region you are going to play
- It installs wine-ge-lol with FSYNC/FUTEX2 support enabled by default for better CPU performance
- Installs the latest DXVK version to translate DirectX 9 and 11 to Vulkan for better performance
- It creates a desktop file in the system menu (with icons for the game)
- Creates an uninstaller in case you want to nuke the game, after you rage quit a match that your teammates did everything they could to make you lose
- Users of hybrid graphics can choose at install time if they want to use the dGPU or not

## <a name="dependencies"></a> Dependencies (install those packages system-wide first):
- `winetricks`
- `wget` (Bash script)
- `kdialog` (Bash script)
- `tar`
- `python`, `python-requests` and `python-psutil` (Python script)
- `qt5-base` and `pyqt5` (Python script)
- WINE 32-64 bits and its [Dependency hell](https://www.gloriouseggroll.tv/how-to-get-out-of-wine-dependency-hell/)

## Remaining tasks:
- Flatpak it

## Can i uninstall the game?
- You can with the Python script, as it will generate an `uninstall.py` file in the directory you installed the game.

## Buy me a coffee

<a href="https://www.paypal.com/donate/?hosted_button_id=UMJWYGDH2RC7E"><img src="https://github.com/andreostrovsky/donate-with-paypal/blob/master/grey.svg" alt="Donate with PayPal" width="150" height="40"></a>

