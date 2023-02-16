#!/bin/bash

# Function for logging messages to file
function log_message() {
  message="$1"
  timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  echo "[$timestamp] $message" | tee -a "$leagueoflegends_dir/leagueoflegends.log"
}

# Create leagueoflegends directory in home directory if it doesn't exist
leagueoflegends_dir="$HOME/leagueoflegends"
if [ ! -d "$leagueoflegends_dir" ]; then
  mkdir "$leagueoflegends_dir"
  log_message "Created directory $leagueoflegends_dir"
fi

# Create Downloads directory in leagueoflegends directory
downloads_dir="$leagueoflegends_dir/Downloads"
if [ -d "$downloads_dir" ]; then
  rm -rf "$downloads_dir"
  log_message "Removed directory $downloads_dir"
fi
mkdir "$downloads_dir"
log_message "Created directory $downloads_dir"

# Download League installer file and wine translation layer for League
league_installer_url="https://lol.secure.dyn.riotcdn.net/channels/public/x/installer/current/live.br.exe"
wine_lutris_ge_lol_url="https://github.com/GloriousEggroll/wine-ge-custom/releases/download/7.0-GE-5-LoL/wine-lutris-ge-lol-7.0-5-x86_64.tar.xz"

log_message "Downloading files..."
wget -P "$downloads_dir" "$league_installer_url"
wget -P "$downloads_dir" "$wine_lutris_ge_lol_url"
log_message "Finished downloading files"

# Extract wine translation layer file to wine directory
wine_dir="$leagueoflegends_dir/wine"
if [ -d "$wine_dir" ]; then
  rm -rf "$wine_dir"
  log_message "Removed directory $wine_dir"
fi
mkdir "$wine_dir"
log_message "Created directory $wine_dir"
tar -xf "$downloads_dir/wine-lutris-ge-lol-7.0-5-x86_64.tar.xz" -C "$wine_dir" --strip-components=1

# Rename League installer file to leagueinstaller.exe
league_installer_file="$downloads_dir/live.br.exe"
league_installer_name="leagueinstaller.exe"
mv "$league_installer_file" "$downloads_dir/$league_installer_name"
log_message "Renamed $league_installer_file to $league_installer_name"

# Rename wine directory subfolder to wine-lol-lutris
for subfolder in "$wine_dir"/*; do
  if [[ $subfolder == *"lutris-ge-lol-"* ]]; then
    wine_lol_lutris_dir="$wine_dir/wine-lol-lutris"
    mv "$subfolder" "$wine_lol_lutris_dir"
    log_message "Renamed $subfolder to $wine_lol_lutris_dir"
    break
  fi
done

# Create prefix directory inside wine directory
prefix_dir="$wine_dir/prefix"
if [ ! -d "$prefix_dir" ]; then
  mkdir "$prefix_dir"
  log_message "Created directory $prefix_dir"
fi

# Create and run first-boot script
log_message "Creating first-boot script"

cd $leagueoflegends_dir
leaguefirstboot="Firstboot.sh"
touch $leaguefirstboot
chmod +x $leaguefirstboot

echo '#!/bin/bash
export PATH=$HOME/leagueoflegends/wine/bin:$PATH
export WINEPREFIX=$HOME/leagueoflegends/wine/prefix
export WINEDLLOVERRIDES=winemenubuilder.exe=d
export WINELOADER=$HOME/leagueoflegends/wine/bin/wine
export WINEFSYNC=1
export WINEDEBUG=-all
winetricks dxvk &
wait
wine $HOME/leagueoflegends/Downloads/leagueinstaller.exe
sleep 120
exit 0' > $leaguefirstboot

wait

# Launching first-boot script
log_message "Launching the first-boot script, it will wait 120 seconds for the user to press the install button before killing itself"
bash $leagueoflegends_dir/Firstboot.sh &

wait
log_message "Finished first boot"

# Create Launch game .sh script
log_message "Creating Launch.sh script"
cd $leagueoflegends_dir

leaguelauncherfile="Launch.sh"
touch $leaguelauncherfile
chmod +x $leaguelauncherfile

echo '#!/bin/bash
export PATH=$HOME/leagueoflegends/wine/bin:$PATH
export WINEPREFIX=$HOME/leagueoflegends/wine/prefix
export WINELOADER=$HOME/leagueoflegends/wine/bin/wine
export WINEFSYNC=1
export WINEDEBUG=-all
export WINEDLLOVERRIDES=winemenubuilder.exe=d
cd $HOME/leagueoflegends/wine/prefix/drive_c/Riot\ Games/Riot\ Client/
exec wine "RiotClientServices.exe"  --launch-product=league_of_legends --launch-patchline=live' > $leaguelauncherfile

log_message "Launch.sh file created in $leagueoflegends_dir"

# Create system menu shortcut
log_message "Creating menu shortcut for launch script"

cd $HOME/.local/share/applications
touch "LeagueofLegendsKassinlauncher.desktop"
chmod +x "LeagueofLegendsKassinlauncher.desktop"

echo '[Desktop Entry]
Name=League of Legends Kassin Launcher
Comment=Launch League of Legends with the Kassin Launcher
Exec=/bin/bash -c "$HOME/leagueoflegends/Launch.sh"
Terminal=false
Icon=leagueicon.png
Type=Application
Categories=Game;' > LeagueofLegendsKassinlauncher.desktop

log_message "System menu shortcut created"

# Download leaguepng icon from github
wget -O ~/leagueoflegendsicon.png https://github.com/kassindornelles/lol-for-linux-bash-installer/raw/main/leagueoflegendsicon.png
mkdir -p ~/.local/share/icons/hicolor/256x256/
cp ~/leagueoflegendsicon.png ~/.local/share/icons/hicolor/256x256/apps/
log_message "Created league icon in local share icons"

# Launch the Launch.sh script

bash $leagueoflegends_dir/Launch.sh
log_message "All finished! have fun :)"
