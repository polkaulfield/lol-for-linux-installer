# lol-for-linux-installer

League of Legends unofficial installer/manager for linux

<b>This software is not affiliated with nor supported by Riot Games.</b>

<noscript><a href="https://liberapay.com/kassindornelles/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a></noscript> <a href="https://www.paypal.com/donate/?hosted_button_id=UMJWYGDH2RC7E"><img src="https://github.com/andreostrovsky/donate-with-paypal/blob/master/grey.svg" alt="Donate with PayPal" width="150" height="40"></a>

### Features:
- Choose where to install the game (as long as the directory is writable by current user)
- wine-ge-lol with ESYNC/FSYNC/FUTEX2 support enabled by default for better CPU performance
- Desktop file in the system menu
- Options for the use of dGPU/APU/SecondaryGPU
- obs-gamecapture support
- vkBasalt CAS (Sharpening filter) support with a slider for sharpness strength
- You can change between the Wine builds supported
- DXVK version management
- Feral Gamemode support
- Discord Rich Presence support (Thanks to @JocarLixo and @daglaroglou)

### GPU's and Drivers suppported:
Check for it in the [DXVK Driver support wiki page](https://github.com/doitsujin/dxvk/wiki/Driver-support)


## <a name="dependencies"></a> Dependencies:

### Necessary Dependencies:

`python` `python-psutil` `python-pyqt5` `python-cffi` `wine` `python-requests` `qt5-base` `tar` `lib32-gnutls` `gnutls` `lib32-libldap` `libldap` `libpng` `lib32-libpng` `mesa` `lib32-mesa` `libgphoto2` `libpulse` `lib32-libpulse` `python-pip`

### Optional dependencies:

- `vkbasalt`: Enables additional visual enhancements, 
- `gamemode`: Improves game performance', 
- `mangohud`: Provides an overlay with game performance metrics')

 ** Different distributions have different names for packages
   
- WINE and its [Dependency hell](https://www.gloriouseggroll.tv/how-to-get-out-of-wine-dependency-hell/)


## Easy installation
- For <b>Ubuntu/Mint/Pop_OS!</b> users we provide .deb packages, those are basically double-click and install, they are available in the [release page](https://github.com/kassindornelles/lol-for-linux-installer/releases)

Important to notice that Ubuntu 23.04 is broken and we don't currently support it.
  
- For <b>Arch Linux/Manjaro/EndeavourOS</b> users we have a PKGBUILD, just run "makepkg -si" in a terminal or get the package from the [release page](https://github.com/kassindornelles/lol-for-linux-installer/releases), grab the file that ends with `pkg.tar.zst` and install it using `sudo pacman -U package_name_here.pkg.tar.zst`
  
- For <b>Fedora 38</b> download the .rpm file in the [release page](https://github.com/kassindornelles/lol-for-linux-installer/releases) and double click it.

- If you want to build the packages yourself or contribute to improve the packaging system check the [Packaging repository](https://github.com/kassindornelles/lol-for-linux-installer-packages)



## Contributions needed for:
- Flatpak package
- Arch Linux AUR inclusion

## Interface and options:
![Screenshot_20230804_160227](https://github.com/kassindornelles/lol-for-linux-installer/assets/40970965/f3730fd6-7e1c-4d7e-a090-01e270ecebf4)
![Screenshot_20231024_232300](https://github.com/kassindornelles/lol-for-linux-installer/assets/40970965/00ba2c8e-9809-457f-8f4e-7c15163c291a)
![Screenshot_20231024_232341](https://github.com/kassindornelles/lol-for-linux-installer/assets/40970965/181526ed-92a3-4814-bf43-1d70c906ce44)
![Screenshot_20231024_232343](https://github.com/kassindornelles/lol-for-linux-installer/assets/40970965/4cc9eb47-b97a-4371-aaa0-3cf534abe4b4)
![Screenshot_20231024_232346](https://github.com/kassindornelles/lol-for-linux-installer/assets/40970965/e24358a9-bda5-42f0-a0d3-5a406b6b0269)


## FAQ:

- This project <b>DOES NOT manage League of Legends installations that were done via Lutris or any other source</b>, we do the installation ourselves and we handle our own installation and ONLY it.

- <b> Don't demand features in the bug tracker, open a pull request instead and contribute with code</b>, depending of the amount of work i might be able to pull it off but if things get super complex or are super niche i won't be able to do it.

- The .svg icon that this application uses is provided by the [papirus-icon-theme project](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme)

