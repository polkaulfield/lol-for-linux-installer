#!/usr/bin/env python3
import os, shutil, requests, tarfile, subprocess, json, logging, urllib.request
from PyQt5.QtCore import pyqtSignal, QObject

def install_dxvk_code(game_main_dir):
        dst_path = os.path.join(game_main_dir, 'wine', 'prefix', 'drive_c', 'windows')
        tmp_path = 'dxvk-tmp'
        url = 'https://github.com/doitsujin/dxvk/releases/download/v1.10.3/dxvk-1.10.3.tar.gz'
        filename = os.path.basename(url)
        urllib.request.urlretrieve(url, filename)

        with tarfile.open(filename, 'r:gz') as tar:
            tar.extractall(tmp_path)

        for arch in ['x64', 'x32']:
            src_path = os.path.join(tmp_path, 'dxvk-1.10.3', arch)
            dst_path_arch = os.path.join(dst_path, 'system32' if arch == 'x64' else 'syswow64')

            if not os.path.exists(dst_path_arch):
                os.makedirs(dst_path_arch)

            for file_name in os.listdir(src_path):
                if file_name.endswith('.dll'):
                    src_file = os.path.join(src_path, file_name)
                    dst_file = os.path.join(dst_path_arch, file_name)
                    shutil.copy2(src_file, dst_file)

        os.remove(filename)
        shutil.rmtree(tmp_path)

def league_install_code(game_main_dir, game_region_link):

    # Expose variables
    logging.info("Setting all variables")  # Cheap logging
    wine_version = "wine-build"
    home_dir = os.environ.get('XDG_CONFIG_HOME') or os.path.expanduser('~/')
    game_downloads_dir = os.path.join(game_main_dir, 'downloads')
    game_main_wine_dir = os.path.join(game_main_dir, 'wine')
    game_prefix_dir = os.path.join(game_main_wine_dir, 'prefix')
    user_local_share = os.path.join(home_dir, ".local/share")
    game_launch_file_path = os.path.join(game_main_dir, "launch-league-of-legends.py")
    user_config_folder= os.path.join(home_dir, ".config")
    wine_loader_path = os.path.join(game_main_wine_dir, 'wine-build', 'bin', 'wine')

    # Create all folders that we are going to use
    folder_paths = [game_main_dir, game_downloads_dir, game_main_wine_dir, game_prefix_dir, user_config_folder]
    logging.info("Creating folders for our League install")  # Cheap logging
    for folder_path in folder_paths:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            os.chmod(folder_path, 0o700)

    # Download necessary files
    logging.info("Downloading wine-lutris-lol build")  # Cheap logging
    wine_lutris_build_url = "https://github.com/GloriousEggroll/wine-ge-custom/releases/download/8.7-GE-1-LoL/wine-lutris-ge-lol-8.7-1-x86_64.tar.xz"
    tar_file_name = wine_version + ".tar.xz"
    wine_lutris_build_file = os.path.join(game_downloads_dir, tar_file_name)
    response = requests.get(wine_lutris_build_url)
    with open(wine_lutris_build_file, "wb") as f:
        f.write(response.content)

    logging.info("Downloading League of Legends installer from " + game_region_link)  # Cheap logging
    exe_file_name = "lolinstaller.exe"
    league_installer_file = os.path.join(game_downloads_dir, exe_file_name)
    response = requests.get(game_region_link)
    with open(league_installer_file, "wb") as f:
        f.write(response.content)

    logging.info("All files Downloaded")  # Cheap logging

    # Extract tar file
    logging.info("Extracting the wine-lutris-lol build file")
    with tarfile.open(os.path.join(game_downloads_dir, tar_file_name)) as file:
        file.extractall(path=game_main_wine_dir)
        extracted_folder_name = file.getnames()[0]
    os.rename(os.path.join(game_main_wine_dir, extracted_folder_name), os.path.join(game_main_wine_dir, "wine-build"))
    logging.info("Extraction of the wine-lutris-lol build file completed")

    with open('env_vars.json', 'r') as env_vars_file:
        env_vars = json.load(env_vars_file)
        game_launcher_options = env_vars.get("game_launcher_options", {})

    # Replace placeholders in game launcher options with actual values
    game_launcher_options['PATH'] = os.path.join(game_main_wine_dir, 'wine-build', 'bin')
    game_launcher_options['WINEPREFIX'] = game_prefix_dir
    game_launcher_options['WINELOADER'] = wine_loader_path

    first_boot_envs = dict(os.environ, **game_launcher_options)
    subprocess.run(["wine", league_installer_file], env=first_boot_envs, check=True)

    # Create a dictionary to hold the install dir data
    data_folder = {
        "game_main_dir": game_main_dir
    }

    # Write the dictionary to a JSON file in the user_config_folder directory
    with open(os.path.join(user_config_folder, "league_install_path.json"), "w") as outfile:
        json.dump(data_folder, outfile)

    logging.info("json file created")

    # Create the directory if it doesn't exist
    os.makedirs(user_config_folder, exist_ok=True)

    # Wine build version json
    lol_build_current = {
        "current_build_name": wine_lutris_build_url
    }

    with open(os.path.join(game_main_dir, "buildversion.json"), "w") as outfile:
        json.dump(lol_build_current, outfile)

    logging.info("LoL build json file created")

    # Delete downloads folder
    try:
        shutil.rmtree(game_downloads_dir)
    except FileNotFoundError:
        logging.warning(f"Directory {game_downloads_dir} does not exist")
    logging.info("Downloads folder deletion")

    # Copy launcher
    try:
        shutil.copy("lol-for-linux-installer.py", os.path.join(game_main_dir, "lol-for-linux-installer.py"))
        shutil.copy("python_src/ui/installer.ui", os.path.join(game_main_dir, "python_src", "ui", "installer.ui"))
        shutil.copy("python_src/ui/lolbanner.jpeg", os.path.join(game_main_dir, "python_src", "ui", "lolbanner.jpeg"))
        shutil.copy("leagueinstaller_code.py", os.path.join(game_main_dir, "leagueinstaller_code.py"))
    # Fallback for PKGBUILD/AppImage/Others
    except:
        logging.warning("Not copying any files, packing format is in use")
    logging.info("Copied launcher")

    install_dxvk_code(game_main_dir)
