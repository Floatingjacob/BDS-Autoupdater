import os
import requests
import subprocess
import sys
import re

BDS_DOWNLOAD_PAGE = "https://www.minecraft.net/en-us/download/server/bedrock"
DOWNLOAD_FOLDER = "updatetemp"
SERVER_EXECUTABLE = "bedrock_server.exe"
BDS_BASE_URL = "https://www.minecraft.net/bedrockdedicatedserver/bin-win/"
SERVER_DIRECTORY = "."
ZIP_PATH = os.path.join(DOWNLOAD_FOLDER, "bds.zip")
VERSION_LOG = "bds_version.txt"

TOOLS_FOLDER = "tools"
CLEAN_BAT = "clean.bat"
UPDATE_BAT = "update.bat"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_latest_bds_version():
    try:
        print("[INFO] Fetching latest BDS version number...")
        response = requests.get(BDS_DOWNLOAD_PAGE, headers=HEADERS, timeout=30)
        response.raise_for_status()
        match = re.search(r'bedrock-server-(\d+\.\d+\.\d+\.\d+)\.zip', response.text)
        if match:
            latest_version = match.group(1)
            print(f"[INFO] Latest BDS version found: {latest_version}")
            return latest_version
        else:
            raise ValueError("Could not find the latest BDS version number.")
    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out. Retrying...")
        return get_latest_bds_version()
    except Exception as e:
        print(f"[ERROR] Failed to fetch latest version: {e}")
        sys.exit(1)

def get_installed_bds_version():
    if os.path.exists(VERSION_LOG):
        with open(VERSION_LOG, "r") as file:
            return file.read().strip()
    return None

def save_installed_bds_version(version):
    with open(VERSION_LOG, "w") as file:
        file.write(version)

def construct_bds_download_url(latest_version):
    return f"{BDS_BASE_URL}bedrock-server-{latest_version}.zip"

def download_bds(download_url):
    try:
        os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
        print(f"[INFO] Downloading BDS from {download_url}...")
        response = requests.get(download_url, stream=True, headers=HEADERS, timeout=60)
        response.raise_for_status()
        
        with open(ZIP_PATH, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("[INFO] Download completed successfully.")
    except requests.exceptions.Timeout:
        print("[ERROR] Download timed out. Retrying...")
        download_bds(download_url)
    except Exception as e:
        print(f"[ERROR] Failed to download BDS: {e}")
        sys.exit(1)

def update_bds():
    latest_version = get_latest_bds_version()
    installed_version = get_installed_bds_version()
    
    if installed_version == latest_version:
        print(f"[INFO] Installed version ({installed_version}) is already up to date.")
    else:
        latest_bds_url = construct_bds_download_url(latest_version)
        print("[INFO] Stopping server...")
        os.system(f'taskkill /IM "{SERVER_EXECUTABLE}" /F 2>nul')
        download_bds(latest_bds_url)
        print("[INFO] Running update.bat to extract new files...")
        subprocess.run([UPDATE_BAT], check=True)
        save_installed_bds_version(latest_version)
        print(f"[INFO] Updated to version {latest_version}")
        print(f"[INFO] Deleting used update file")
        subprocess.run([CLEAN_BAT], check=True)
        
    print("[INFO] Restarting Minecraft Bedrock server...")
    subprocess.Popen([SERVER_EXECUTABLE], creationflags=subprocess.CREATE_NEW_CONSOLE)

update_bds()
