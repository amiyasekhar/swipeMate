import os
import sys
import subprocess

def install_chrome_linux():
    print("Installing Google Chrome on Linux...")
    try:
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "wget"], check=True)
        subprocess.run(
            ["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"],
            check=True
        )
        subprocess.run(["sudo", "apt", "install", "-y", "./google-chrome-stable_current_amd64.deb"], check=True)
        print("Google Chrome installed successfully on Linux.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Google Chrome on Linux: {e}")
        sys.exit(1)

def install_chrome_macos():
    print("Installing Google Chrome on macOS...")
    try:
        subprocess.run(["brew", "install", "--cask", "google-chrome"], check=True)
        print("Google Chrome installed successfully on macOS.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Google Chrome on macOS: {e}")
        sys.exit(1)

def install_chrome_windows():
    print("Installing Google Chrome on Windows...")
    try:
        # Download Chrome installer
        installer_url = "https://dl.google.com/chrome/install/latest_chrome_installer.exe"
        installer_path = os.path.join(os.getcwd(), "ChromeInstaller.exe")
        subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri {installer_url} -OutFile {installer_path}"], check=True)
        
        # Run the installer
        subprocess.run(["msiexec", "/i", installer_path, "/quiet", "/norestart"], check=True)
        print("Google Chrome installed successfully on Windows.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Google Chrome on Windows: {e}")
        sys.exit(1)