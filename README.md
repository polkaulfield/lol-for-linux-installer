# lol-for-linux-installer

League of Legends unofficial installer/manager for linux

This software is not affiliated with nor supported by Riot Games.
![Screenshot_20230526_122858](https://github.com/kassindornelles/lol-for-linux-installer/assets/40970965/b77e576b-5044-4447-bea2-06cb80da3a3c)
![Screenshot_20230527_131038](https://github.com/kassindornelles/lol-for-linux-installer/assets/40970965/d8192248-aa45-46e3-bbd6-ba2bdca660b2)


## Easy installation
- We provide .deb packages now (PKGBUILD + makedeb) since v.2.3, so if you are in a ubuntu based distro go ahead and use it

 Most known Ubuntu based distributions: Linux Mint, Pop_OS!, ElementaryOS and many others.

- For Arch Linux users we have a PKGBUILD, just run "makepkg -si" in a terminal

 Should work fine on EndeavourOS, Manjaro and others
 
 ## In order for the game client to launch you NEED to install DXVK using our UI! (the "Renderer" option).

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

   On ubuntu-based distributions the python packages are called "python3-psutil, python3-requests and python3-pyqt5"
   
- WINE 32-64 bits and its [Dependency hell](https://www.gloriouseggroll.tv/how-to-get-out-of-wine-dependency-hell/)

## Contributions needed for:
- Flatpak package
- Arch Linux AUR inclusion
- Fedora packaging

## Buy me a coffee

<a href="https://www.paypal.com/donate/?hosted_button_id=UMJWYGDH2RC7E"><img src="https://github.com/andreostrovsky/donate-with-paypal/blob/master/grey.svg" alt="Donate with PayPal" width="150" height="40"></a>

