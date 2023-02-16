#!/usr/bin/env bash

# XDG stuff
[ ! -d "${XDG_DATA_HOME}" ] && XDG_DATA_HOME=~/.local/share

# Step 1: Check if leagueoflegends directory and Launch.sh script exist
if [ -d "${XDG_DATA_HOME}/leagueoflegends" ] && [ -f "${XDG_DATA_HOME}/leagueoflegends/Launch.sh" ]; then
  # Step 2: Start the Launch.sh script
  echo "League of legends was detected, running the game..."
  cd "${XDG_DATA_HOME}/leagueoflegends"
  chmod +x ./Launch.sh
  ./Launch.sh
else
  # Step 3: Launch leagueinstaller.sh from current directory
  echo "League of legends install not detected, installing the game..."
  chmod +x ./leagueinstaller.sh
  ./leagueinstaller.sh
fi
