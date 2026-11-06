import os
import sys
import subprocess
import urllib.request
import zipfile
import io

GITHUB_REPO = "YOUR_GITHUB_USERNAME/EyzCrypt-Enterprise"
ZIP_URL = f"https://github.com/{GITHUB_REPO}/archive/refs/heads/main.zip"

def install_and_run():
    print("[*] Downloading EyzCrypt Enterprise from GitHub...")
    try:
        # تحميل المشروع كملف zip
        with urllib.request.urlopen(ZIP_URL) as response:
            zip_data = io.BytesIO(response.read())
    except Exception as e:
        print(f"[-] Failed to download: {e}")
        print("Make sure the repository is public and the URL is correct.")
        return

    print("[*] Extracting files...")
    with zipfile.ZipFile(zip_data) as z:
        z.extractall("EyzCrypt_Project")
        
    # الانتقال لمجلد المشروع
    project_dir = os.path.join("EyzCrypt_Project", "EyzCrypt-Enterprise-main")
    os.chdir(project_dir)

    print("[*] Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "flask"], stdout=subprocess.DEVNULL)

    print("[+] Starting EyzCrypt Server...")
    print("[+] Open your browser at: http://127.0.0.1:8080")
    subprocess.run([sys.executable, "app.py"])

if __name__ == "__main__":
    install_and_run()￼Enter
