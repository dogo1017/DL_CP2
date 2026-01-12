import requests, os, sys, time

EXE_NAME = "YourApp.exe"  # name of your main app .exe
DOWNLOAD_URL = "https://github.com/yourusername/yourrepo/releases/latest/download/yourapp.exe"

def update():
    exe_path = os.path.abspath(EXE_NAME)
    temp_path = exe_path + ".tmp"

    print("Downloading update...")
    r = requests.get(DOWNLOAD_URL, stream=True)
    with open(temp_path, "wb") as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)

    print("Waiting for old app to close...")
    time.sleep(2)  # ensure the main app is closed

    # Replace old exe
    os.replace(temp_path, exe_path)
    print("Update complete! Launching new version...")
    os.startfile(exe_path)

if __name__ == "__main__":
    update()
