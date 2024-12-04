import os
import subprocess
import time
import requests
from pychrome import Browser

class ChromeController:
    def __init__(self):
        self.token = None

    def start_and_get_token(self):
        """Start Chrome in debugging mode and retrieve X-Auth-Token."""
        chrome_path = "/path/to/chrome"  # Update this path based on the OS
        debug_port = "9222"
        url = "https://tinder.com"

        try:
            # Start Chrome
            subprocess.Popen([chrome_path, f"--remote-debugging-port={debug_port}", url])
            time.sleep(5)  # Allow time for Chrome to start

            # Connect to Chrome DevTools
            browser = Browser(url=f"http://127.0.0.1:{debug_port}")
            tabs = browser.list_tab()

            for tab in tabs:
                if not tab._started:
                    tab.start()
                if "tinder.com" in tab.url:
                    tab.Network.enable()
                    self.token = self._monitor_requests(tab)
                    return self.token
        except Exception as e:
            raise RuntimeError(f"Error starting Chrome or retrieving token: {e}")

    def _monitor_requests(self, tab):
        """Monitor network requests to extract X-Auth-Token."""
        token = None

        def log_request(**kwargs):
            nonlocal token
            request = kwargs.get("request", {})
            if "api.gotinder.com" in request.get("url", ""):
                headers = request.get("headers", {})
                token = headers.get("X-Auth-Token")

        tab.set_listener("Network.requestWillBeSent", log_request)

        # Wait for token
        for _ in range(10):  # Wait up to 10 seconds
            if token:
                return token
            time.sleep(1)

        raise RuntimeError("X-Auth-Token not found in requests.")

    def send_token_to_backend(self, token):
        """Send the token to the backend."""
        backend_url = "https://swipemate.ai/submit-token"
        response = requests.post(backend_url, json={"token": token})
        return response.text