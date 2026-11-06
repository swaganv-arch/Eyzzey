import os
import sys
import subprocess
import urllib.request
import zipfile
import io

# مستودعك على GitHub
GITHUB_REPO = "swaganv-arch/Eyzzey"
ZIP_URL = f"https://github.com/{GITHUB_REPO}/archive/refs/heads/main.zip"

def install_and_run():
    print(f"[*] Fetching EyzCrypt from GitHub ({GITHUB_REPO})...")
    try:
        # تحميل المشروع كملف zip من GitHub
        req = urllib.request.Request(ZIP_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            zip_data = io.BytesIO(response.read())
    except Exception as e:
        print(f"[-] Failed to download: {e}")
        print("[-] Make sure the repository is Public and the URL is correct.")
        return

    print("[*] Extracting files...")
    extract_dir = "Eyzzey_App"
    with zipfile.ZipFile(zip_data) as z:
        z.extractall(extract_dir)
        
    # الدخول على مجلد المشروع (GitHub بيضيف -main عادة)
    project_dir = os.path.join(extract_dir, "Eyzzey-main")
    if not os.path.exists(project_dir):
        # في حال كان اسم الفرع مختلف
        folders = [f for f in os.listdir(extract_dir) if f.startswith("Eyzzey")]
        if folders:
            project_dir = os.path.join(extract_dir, folders[0])
        else:
            print("[-] Could not find extracted project folder.")
            return

    os.chdir(project_dir)

    print("[*] Installing requirements (Flask)...")
    # تثبيت المكتبات
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], stdout=subprocess.DEVNULL)

    print("\n=============================================")
    print(" [+] Starting EyzCrypt Server...")
    print(" [+] Open your browser and go to: http://127.0.0.1:8080")
    print(" [+] Press Ctrl+C to stop the server.")
    print("=============================================\n")
    
    # تشغيل السيرفر
    subprocess.run([sys.executable, "app.py"])

if __name__ == "__main__":
    install_and_run()
