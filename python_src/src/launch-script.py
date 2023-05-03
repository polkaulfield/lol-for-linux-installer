#!/usr/bin/env python3
import os, subprocess, json, time

cwd = os.getcwd()
game_main_dir = os.path.join(cwd)
game_main_wine_dir = os.path.join(game_main_dir, 'wine')
game_prefix_dir = os.path.join(game_main_wine_dir, 'prefix')
game_exe_path = os.path.join(game_prefix_dir, 'drive_c', 'Riot Games', 'Riot Client')
game_exe_file_name = 'RiotClientServices.exe'
wine_loader_path = os.path.join(game_main_wine_dir, 'wine-build', 'bin', 'wine')
gamescope_envs = []

with open('env_vars.json', 'r') as f:
    env_vars = json.load(f)

# Replace placeholders with actual values
env_vars['PATH'] = os.path.join(game_main_wine_dir, 'wine-build', 'bin')
env_vars['WINEPREFIX'] = game_prefix_dir
env_vars['WINELOADER'] = wine_loader_path

with open('app_settings.json', 'r') as f:
    app_settings = json.load(f)

if app_settings["FSR"] == '1':
    gamescope_envs += ['-U']

if app_settings['Gamescope'] == '1':
    start_game_vars = dict(os.environ, **env_vars)
    wine_process = ["wine", os.path.join(game_exe_path, game_exe_file_name)]
    gamescope_path = subprocess.run(["which", "gamescope"], capture_output=True, text=True).stdout.strip()
    gamescope_process = [gamescope_path] + gamescope_envs + ["--"] + wine_process + ["--launch-product=league_of_legends", "--launch-patchline=live"]
    subprocess.run(gamescope_process, env=start_game_vars, check=True)
else:
    start_game_vars = dict(os.environ, **env_vars)
    wine_process = ["wine", os.path.join(game_exe_path, game_exe_file_name), "--launch-product=league_of_legends", "--launch-patchline=live"]
    subprocess.run(wine_process, env=start_game_vars, check=True)

