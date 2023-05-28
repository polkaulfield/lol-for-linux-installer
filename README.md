# lol-for-linux-installer

League of Legends unofficial installer/manager for linux

This software is not affiliated with nor supported by Riot Games.

![Screenshot_20230526_122858](https://github.com/kassindornelles/lol-for-linux-installer/assets/40970965/b77e576b-5044-4447-bea2-06cb80da3a3c)
![Screenshot_20230528_105742](https://github.com/kassindornelles/lol-for-linux-installer/assets/40970965/b4873226-13e8-4d8f-92e1-428271fa11f6)


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

## Buy me a coffee

<a href="https://www.paypal.com/donate/?hosted_button_id=UMJWYGDH2RC7E"><img src="https://github.com/andreostrovsky/donate-with-paypal/blob/master/grey.svg" alt="Donate with PayPal" width="150" height="40"></a>

