# lol-for-linux-installer

League of Legends unofficial installer/manager for linux

This software is not affiliated with nor supported by Riot Games.

## Installation welcome screen:
![Screenshot_20230528_203841](https://github.com/kassindornelles/lol-for-linux-installer/assets/40970965/dc0d48b9-a1fc-440c-9bbc-28ba47966011)

## After install game management:
![Screenshot_20230528_203911](https://github.com/kassindornelles/lol-for-linux-installer/assets/40970965/0c19955c-a2f6-4109-9c76-be9f6236d71b)



## Easy installation
- For <b>Ubuntu/Mint/Pop_OS!</b> users we provide .deb packages, those are basically double-click and install, they are available in the [release page](https://github.com/kassindornelles/lol-for-linux-installer/releases)
- For <b>Arch Linux/Manjaro/EndeavourOS</b> users we have a PKGBUILD, just run "makepkg -si" in a terminal or get the package from the [release page](https://github.com/kassindornelles/lol-for-linux-installer/releases), grab the file that ends with `pkg.tar.zst` and install it using `sudo pacman -U package_name_here.pkg.tar.zst`

### Python Script features:
- You can choose where to install the game and also the region you are going to play
- It installs wine-ge-lol with FSYNC/FUTEX2 support enabled by default for better CPU performance
- Desktop file in the system menu (assuming you installed it as a system package like .deb, pkg.tar.zst and etc)
- Option to uninstall the game to reinstall in case you have problems
- Users of hybrid graphics can choose at install time if they want to use the dGPU or not
- obs-gamecapture support
- vkBasalt CAS support
- Update system for WINE builds
- DXVK installation
- Gamemode support

## <a name="dependencies"></a> Dependencies:
- `tar`, `python`, `python-requests`, `python-psutil`, `qt5-base` and `pyqt5`

   Different distributions have different names for packages*
   
- WINE and its [Dependency hell](https://www.gloriouseggroll.tv/how-to-get-out-of-wine-dependency-hell/)

## Contributions needed for:
- Flatpak package
- Arch Linux AUR inclusion
- Fedora packaging

## FAQ:
- This project <b>DOES NOT manage League of Legends installations that were done via Lutris or any other source</b>, we do the installation ourselves and we handle our own installation and ONLY it.

- This project is both a installer and a launcher, i know, the name of the project is bad but it is what it is.

- <b> Don't demand features in the bug tracker, open a pull request instead and contribute with code</b>, depending of the amount of work i might be able to pull it off but if things get super complex or are super niche i won't be able to do it.

### I selected the option to skip the launcher but now i need to open it again, how do i do it?

- Navigate to the folder your game is installed and open the file "env_vars.json" with a text editor

- Change the value of `"Skiplauncher": "1"` from `1` to `0`

## Buy me a coffee
If you believe this software saved you some time or solved issues you had playing LoL on Linux then please consider a donation, the cost of my medications is high and i need your support.

<a href="https://www.paypal.com/donate/?hosted_button_id=UMJWYGDH2RC7E"><img src="https://github.com/andreostrovsky/donate-with-paypal/blob/master/grey.svg" alt="Donate with PayPal" width="150" height="40"></a>

