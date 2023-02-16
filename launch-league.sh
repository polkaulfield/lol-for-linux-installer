#!/usr/bin/env bash

# Step 1: Check if leagueoflegends directory and Launch.sh script exist
if [ -d "$HOME/leagueoflegends" ] && [ -f "$HOME/leagueoflegends/Launch.sh" ]; then
  # Step 2: Start the Launch.sh script
  echo "League of legends was detected, running the game..."
  cd "$HOME/leagueoflegends"
  ./Launch.sh
else
  # Step 3: Launch leagueinstaller.sh from current directory
  echo "League of legends install not detected, installing the game..."
  chmod +x ./leagueinstaller.sh
  ./leagueinstaller.sh
fi
