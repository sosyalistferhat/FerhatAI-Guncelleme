
import requests
import os
import sys

GITHUB_REPO_RAW = "https://raw.githubusercontent.com/KULLANICI_ADI/REPO_ADI/main"
LOCAL_VERSION_FILE = "version.txt"
REMOTE_VERSION_URL = f"{GITHUB_REPO_RAW}/version.txt"
REMOTE_MAIN_URL = f"{GITHUB_REPO_RAW}/main.py"

def get_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return "0.0.0"
    with open(LOCAL_VERSION_FILE, "r") as f:
        return f.read().strip()

def get_remote_version():
    try:
        response = requests.get(REMOTE_VERSION_URL, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except Exception as e:
        print(f"Uzak sürüm alınamadı: {e}")
    return None

def update_main_file():
    try:
        response = requests.get(REMOTE_MAIN_URL, timeout=5)
        if response.status_code == 200:
            with open("main.py", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("Güncelleme başarıyla indirildi. Uygulama yeniden başlatılıyor...")
            os.execv(sys.executable, ['python'] + ['main.py'])
    except Exception as e:
        print(f"Güncelleme sırasında hata oluştu: {e}")

def check_for_updates():
    local_version = get_local_version()
    remote_version = get_remote_version()
    if remote_version and remote_version != local_version:
        print(f"Yeni sürüm bulundu: {remote_version} (Şu anki: {local_version})")
        update_main_file()
    else:
        print("Güncel sürüm kullanılıyor.")

if __name__ == "__main__":
    check_for_updates()
