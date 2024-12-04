import os
import platform
import subprocess

def find_chrome_binary():
    """Search the system for a valid Chrome binary."""
    print("Searching system for Google Chrome...")
    common_paths = {
        "Darwin": [  # macOS
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        ],
        "Linux": [  # Linux
            "/usr/bin/google-chrome",
            "/opt/google/chrome/chrome",
            "/usr/bin/google-chrome-stable"
        ],
        "Windows": [  # Windows
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]
    }

    current_os = platform.system()
    if current_os in common_paths:
        for path in common_paths[current_os]:
            if os.path.exists(path):
                print(f"Found Chrome at {path}")
                return path

    # Perform additional searches if not found in common paths
    print("Google Chrome not found in common paths. Performing system-wide search...")
    if current_os == "Darwin":  # macOS
        result = subprocess.run(["mdfind", "kMDItemCFBundleIdentifier == 'com.google.Chrome'"], stdout=subprocess.PIPE, text=True)
        chrome_path = result.stdout.strip()
        if chrome_path and os.path.exists(chrome_path):
            print(f"Found Chrome at {chrome_path}")
            return chrome_path
    elif current_os == "Linux":  # Linux
        result = subprocess.run(["which", "google-chrome"], stdout=subprocess.PIPE, text=True)
        chrome_path = result.stdout.strip()
        if chrome_path and os.path.exists(chrome_path):
            print(f"Found Chrome at {chrome_path}")
            return chrome_path
    elif current_os == "Windows":  # Windows
        for root in ["C:\\", "D:\\"]:
            for dirpath, _, filenames in os.walk(root):
                for filename in filenames:
                    if filename.lower() == "chrome.exe":
                        chrome_path = os.path.join(dirpath, filename)
                        print(f"Found Chrome at {chrome_path}")
                        return chrome_path

    print("Google Chrome not found on this system.")
    return None