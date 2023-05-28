# lol-for-linux-installer

League of Legends unofficial installer/manager for linux

This software is not affiliated with nor supported by Riot Games.

![Screenshot_20230526_122858](https://github.com/kassindornelles/lol-for-linux-installer/assets/40970965/b77e576b-5044-4447-bea2-06cb80da3a3c)
![Screenshot_20230527_231359](https://github.com/kassindornelles/lol-for-linux-installer/assets/40970965/d4f6c860-a81a-4e7e-a704-a7196061537a)

## Easy installation
- For <b>Ubuntu/Mint/Pop_OS!</b> users we provide .deb packages, those are basically double-click and install, they are available in the [release page](https://github.com/kassindornelles/lol-for-linux-installer/releases)
- For <b>Arch Linux/Manjaro/EndeavourOS</b> users we have a PKGBUILD, just run "makepkg -si" in a terminal or get the package from the [release page](https://github.com/kassindornelles/lol-for-linux-installer/releases), grab the file that ends with `pkg.tar.zst` and install it using `sudo pacman -U package_name_here.pkg.tar.zst`
 
 ### In order for the game client to launch you NEED to install DXVK using our UI! (the "Renderer" option).

### Python Script features:
- You can choose where to install the game and also the region you are going to play
- It installs wine-ge-lol with FSYNC/FUTEX2 support enabled by default for better CPU performance
- It creates a desktop file in the system menu (with icons for the game)
- Option to uninstall the game
- Users of hybrid graphics can choose at install time if they want to use the dGPU or not
- obs-gamecapture support.
- Update system for WINE builds, DXVK version selection and more (DXVK installation via our launcher)
- Gamemode support, if installed system wide it will be used automatically.

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

