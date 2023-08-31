# lol-for-linux-installer

League of Legends unofficial installer/manager for linux

<b>This software is not affiliated with nor supported by Riot Games.</b>

## Interface and options:
![Screenshot_20230804_160227](https://github.com/kassindornelles/lol-for-linux-installer/assets/40970965/f3730fd6-7e1c-4d7e-a090-01e270ecebf4)
![Screenshot_20230804_160159](https://github.com/kassindornelles/lol-for-linux-installer/assets/40970965/9f8acfe2-bb92-4f10-9bf1-5e510c353cf4)
![Screenshot_20230831_183108](https://github.com/kassindornelles/lol-for-linux-installer/assets/40970965/d8a78a9a-3af1-4dce-86dc-275a2a97580b)
![Screenshot_20230804_160209](https://github.com/kassindornelles/lol-for-linux-installer/assets/40970965/5145c89e-1650-4e51-9078-3faaa769da36)


## Easy installation
- For <b>Ubuntu/Mint/Pop_OS!</b> users we provide .deb packages, those are basically double-click and install, they are available in the [release page](https://github.com/kassindornelles/lol-for-linux-installer/releases)

Important to notice that Ubuntu 23.04 is broken and we don't currently support it.
  
- For <b>Arch Linux/Manjaro/EndeavourOS</b> users we have a PKGBUILD, just run "makepkg -si" in a terminal or get the package from the [release page](https://github.com/kassindornelles/lol-for-linux-installer/releases), grab the file that ends with `pkg.tar.zst` and install it using `sudo pacman -U package_name_here.pkg.tar.zst`
  
- For <b>Fedora 38</b> download the .rpm file in the [release page](https://github.com/kassindornelles/lol-for-linux-installer/releases) and double click it.

- If you want to build the packages yourself or contribute to improve the packaging system check the [Packaging repository](https://github.com/kassindornelles/lol-for-linux-installer-packages)

### GPU's and Drivers suppported:
Check for it in the [DXVK Driver support wiki page](https://github.com/doitsujin/dxvk/wiki/Driver-support)

### Features:
- Choose where to install the game (as long as its not outside the Home directory)
- wine-ge-lol with ESYNC/FSYNC/FUTEX2 support enabled by default for better CPU performance
- Desktop file in the system menu
- Option to uninstall the game to reinstall in case you get problems
- Options for the use of dGPU/APU/SecondaryGPU
- obs-gamecapture support
- vkBasalt CAS (Sharpening filter) support with a slider for sharpness strength
- Update system for WINE builds
- DXVK installation, 1.10.3 is used by default for better compatibility with older GPU's that don't support recent vulkan, DXVK 2.1 and 2.2 are available
- Feral Gamemode support

## <a name="dependencies"></a> Dependencies:

### Necessary Dependencies:

`python` `python-psutil` `python-pyqt5` `python-cffi` `wine` `python-requests` `qt5-base` `tar` `lib32-gnutls` `gnutls` `lib32-libldap` `libldap` `libpng` `lib32-libpng` `mesa` `lib32-mesa` `libgphoto2` `libpulse` `lib32-libpulse`

### Optional dependencies:

- `vkbasalt`: Enables additional visual enhancements, 
- `gamemode`: Improves game performance', 
- `mangohud`: Provides an overlay with game performance metrics')

 ** Different distributions have different names for packages
   
- WINE and its [Dependency hell](https://www.gloriouseggroll.tv/how-to-get-out-of-wine-dependency-hell/)

## Contributions needed for:
- Flatpak package
- Arch Linux AUR inclusion

## FAQ:
- Is this project now dead?

<b>No, i'll be doing maintenance when it breaks</b>, newer wine builds, newer packages, but only when stuff breaks, we are feature complete at this point.

- This project <b>DOES NOT manage League of Legends installations that were done via Lutris or any other source</b>, we do the installation ourselves and we handle our own installation and ONLY it.

- This project is both a installer and a launcher, i know, the name of the project is bad but it is what it is.

- <b> Don't demand features in the bug tracker, open a pull request instead and contribute with code</b>, depending of the amount of work i might be able to pull it off but if things get super complex or are super niche i won't be able to do it.

- The .svg icon that this application uses is provided by the [papirus-icon-theme project](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme)

## Buy me a coffee
If you believe this software saved you some time or solved issues you had playing LoL on Linux then please consider a donation.

<a href="https://www.paypal.com/donate/?hosted_button_id=UMJWYGDH2RC7E"><img src="https://github.com/andreostrovsky/donate-with-paypal/blob/master/grey.svg" alt="Donate with PayPal" width="150" height="40"></a>

