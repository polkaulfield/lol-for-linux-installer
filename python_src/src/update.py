#!/usr/bin/env python3
import json, sys, tarfile, shutil, os, urllib.request

url = "https://raw.githubusercontent.com/kassindornelles/lol-for-linux-installer/main/wine_build.json"

filename = "wine_build.json"
urllib.request.urlretrieve(url, filename)

with open(filename, "r") as f:
    data = json.load(f)

with open("buildversion.json", "r") as f:
    existing_data = json.load(f)

print("Value of wine_build.json:", data["current_build_name"])
print("Value of buildversion.json:", existing_data["current_build_name"])

if data["current_build_name"].split("/")[-1] > existing_data["current_build_name"].split("/")[-1]:
    print("Update needed")

    build_url = data["current_build_name"]
    build_filename = build_url.split("/")[-1]
    urllib.request.urlretrieve(build_url, build_filename)

    temp_dir = "tmp"
    os.makedirs(temp_dir, exist_ok=True)
    with tarfile.open(build_filename, "r:xz") as tar:
        tar.extractall(path=temp_dir)

    wine_build_dir = "wine/wine-build"
    if os.path.exists(wine_build_dir):
        shutil.rmtree(wine_build_dir)

    extract_path = os.path.join(temp_dir, os.listdir(temp_dir)[0])
    shutil.move(extract_path, wine_build_dir)

    existing_data["current_build_name"] = data["current_build_name"]
    with open("buildversion.json", "w") as f:
        json.dump(existing_data, f)

else:
    print("No need to update")
    sys.exit(0)

os.remove(filename)
if os.path.exists(build_filename):
    os.remove(build_filename)
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)
