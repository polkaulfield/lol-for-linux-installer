#!/usr/bin/env python3
import json, urllib.request, os, re

url = "https://raw.githubusercontent.com/kassindornelles/lol-for-linux-installer/main/wine_build.json"

filename = "wine_build.json"
urllib.request.urlretrieve(url, filename)

with open(filename, "r") as f:
    data = json.load(f)

with open("buildversion.json", "r") as f:
    existing_data = json.load(f)

current_version = re.search(r"(\d+\.\d+)-GE-(\d+)-LoL/wine-lutris-ge-lol-(\d+\.\d+\.\d+)-x86_64.tar.xz", data["current_build_name"]).group(3)
existing_version = re.search(r"(\d+\.\d+)-GE-(\d+)-LoL/wine-lutris-ge-lol-(\d+\.\d+\.\d+)-x86_64.tar.xz", existing_data["current_build_name"]).group(3)

print("Value of wine_build.json:", current_version)
print("Value of buildversion.json:", existing_version)

if current_version <= existing_version:
    print("No need to update")
else:
    print("Update needed")

os.remove(filename)
