import os
import sys
import time
import subprocess
import platform
import requests
import threading
import pychrome
from flask import Flask, jsonify
from flask_cors import CORS
import shutil

# Disable proxies for local connections
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

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
        installer_url = "https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7B014E2B74-3179-7E56-C5E6-1D0EB2E7D214%7D%26lang%3Den%26browser%3D4%26usagestats%3D0%26appname%3DChrome%26needsadmin%3Dtrue/edgedl/chrome/install/GoogleChromeStandaloneEnterprise64.msi"
        installer_path = os.path.join(os.getcwd(), "ChromeInstaller.msi")
        subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri {installer_url} -OutFile {installer_path}"], check=True)
        
        # Run the installer
        subprocess.run(["msiexec", "/i", installer_path, "/quiet", "/norestart"], check=True)
        print("Google Chrome installed successfully on Windows.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Google Chrome on Windows: {e}")
        sys.exit(1)


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
            print(f"Searching {root} drive for Chrome...")
            for dirpath, _, filenames in os.walk(root):
                for filename in filenames:
                    if filename.lower() == "chrome.exe":
                        chrome_path = os.path.join(dirpath, filename)
                        print(f"Found Chrome at {chrome_path}")
                        return chrome_path

    print("Google Chrome not found on this system.")
    return None


def start_browser_with_debugging(browser_name):
    if browser_name != "chrome":
        print(f"Unsupported browser: {browser_name}")
        sys.exit(1)

    print(f"Starting {browser_name} with debugging...")

    chrome_path = find_chrome_binary()
    if not chrome_path:
        current_os = platform.system()
        print(f"No Chrome installation found on {current_os}. Attempting to install...")
        if current_os == "Linux":
            install_chrome_linux()
        elif current_os == "Darwin":
            install_chrome_macos()
        elif current_os == "Windows":
            install_chrome_windows()
        else:
            print(f"Unsupported operating system: {current_os}")
            sys.exit(1)

        # Retry finding Chrome after installation
        chrome_path = find_chrome_binary()
        if not chrome_path:
            print(f"Failed to find or install Chrome on {current_os}.")
            sys.exit(1)

    try:
        cmd = [
            chrome_path,
            "--remote-debugging-port=9222",
            "https://tinder.com/"
        ]
        subprocess.Popen(cmd)
        print(f"Chrome started with remote debugging on port 9222 and navigated to Tinder using {chrome_path}.")
    except Exception as e:
        print(f"Failed to start Chrome: {e}")
        sys.exit(1)


def monitor_chrome_requests():
    import pychrome
    import threading
    import time

    x_auth_token = None

    try:
        # Connect to Chrome DevTools
        browser = pychrome.Browser(url="http://127.0.0.1:9222")
        tabs = browser.list_tab()
        print("Tabs open: ", tabs)

        tinder_tab = None
        for tab in tabs:
            # Start the tab before accessing methods
            if not tab._started:
                tab.start()
            target_info = tab.call_method("Target.getTargetInfo")
            url = target_info.get('targetInfo', {}).get('url', '')
            print(f"Tab URL: {url}")
            if 'tinder.com' in url:
                tinder_tab = tab
                break
            # Stop the tab if it's not the one we're looking for
            tab.stop()

        if not tinder_tab:
            print("Tinder.com is not open in any tab. Opening a new tab to navigate to Tinder.")
            # Open a new tab and navigate to Tinder.com
            tinder_tab = browser.new_tab()
            tinder_tab.start()
            load_event_fired = threading.Event()

            def on_load_event_fired(**kwargs):
                load_event_fired.set()

            tinder_tab.Page.loadEventFired = on_load_event_fired
            tinder_tab.Page.enable()
            tinder_tab.Page.navigate(url="https://tinder.com/")
            # Wait for the page to load or timeout after 10 seconds
            load_event_fired.wait(10)
        else:
            if not tinder_tab._started:
                tinder_tab.start()

        # Start monitoring
        tinder_tab.Network.enable()

        auth_token_found = threading.Event()

        def log_request(**kwargs):
            nonlocal x_auth_token
            try:
                request = kwargs.get('request', {})
                # Log all requests
                print(f"Request URL: {request.get('url', '')}")
                # Check if the URL contains the target API endpoint
                if "api.gotinder.com" in request.get('url', ''):
                    print(f"Request detected for URL: {request['url']}")
                    # Extract headers and log them
                    headers = request.get('headers', {})
                    print(f"Request headers: {headers}")
                    # Check for X-Auth-Token in headers
                    x_auth_token = headers.get('X-Auth-Token')
                    if x_auth_token:
                        print(f"X-Auth-Token found in request headers: {x_auth_token}")
                        auth_token_found.set()
                else:
                    print("No X-Auth-Token found in request headers.")
            except Exception as e:
                print(f"Error in log_request: {e}")

        def log_response(**kwargs):
            try:
                response = kwargs.get('response', {})
                if "api.gotinder.com" in response.get('url', ''):
                    print(f"Response detected for {response['url']}")
            except Exception as e:
                print(f"Error in log_response: {e}")

        # Register event handlers using set_listener
        tinder_tab.set_listener("Network.requestWillBeSent", log_request)
        tinder_tab.set_listener("Network.responseReceived", log_response)

        # Process events in a loop
        timeout = 60  # seconds
        start_time = time.time()
        while not auth_token_found.is_set() and (time.time() - start_time) < timeout:
            tinder_tab.wait(1)  # Wait and process events for 1 second

        if x_auth_token:
            print(f"Returned Token: {x_auth_token}")
        else:
            print("Token not found within timeout period.")

        return x_auth_token

    except Exception as e:
        print("Exception occurred in monitor_chrome_requests:")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # Automatically select Chrome for debugging
    browser_choice = 'chrome'

    # Start Chrome in debugging mode
    start_browser_with_debugging(browser_choice)

    # Wait for the browser to start
    time.sleep(5)

    # Monitor Chrome requests
    try:
        token = monitor_chrome_requests()
        print(f"Returned Token: {token}")
    except Exception as e:
        print(f"Error while monitoring requests: {e}")
        sys.exit(1)
