import subprocess
from find_chrome import find_chrome_binary


def start_browser_with_debugging(browser_name):
    if browser_name.lower() != "chrome":
        raise ValueError(f"Unsupported browser: {browser_name}")

    print(f"Starting {browser_name} with debugging...")

    chrome_path = find_chrome_binary()
    if not chrome_path:
        raise FileNotFoundError("Google Chrome binary not found.")

    try:
        cmd = [
            chrome_path,
            "--remote-debugging-port=9222",
            "https://tinder.com/"
        ]
        subprocess.Popen(cmd)
        print(f"Chrome started with remote debugging on port 9222 and navigated to Tinder.")
    except Exception as e:
        raise RuntimeError(f"Failed to start Chrome: {e}")