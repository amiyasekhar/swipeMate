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

# Disable proxies for local connections
os.environ["NO_PROXY"] = "localhost,127.0.0.1"


def get_browser_choice():
    print("Select the browser you are using:")
    print("1. Google Chrome")
    print("2. Mozilla Firefox")
    print("3. Safari")
    choice = input("Enter the number of your choice: ")
    if choice == '1':
        return 'chrome'
    elif choice == '2':
        return 'firefox'
    elif choice == '3':
        return 'safari'
    else:
        print("Invalid choice.")
        sys.exit(1)

def start_browser_with_debugging(browser_name):
    if platform.system() == 'Darwin':  # macOS
        if browser_name == 'chrome':
            cmd = ["open", "-a", "Google Chrome", "--args", "--remote-debugging-port=9222"]
            subprocess.Popen(cmd)
            print("Chrome started with remote debugging on port 9222.")
        elif browser_name == 'firefox':
            cmd = ["open", "-a", "Firefox", "--args", "-start-debugger-server", "6000"]
            subprocess.Popen(cmd)
            print("Firefox started with remote debugging on port 6000.")
        elif browser_name == 'safari':
            print("Starting Safari...")
            print("Please enable 'Allow Remote Automation' in Safari's Develop menu.")
            cmd = ["osascript", "-e", 'tell application "Safari" to activate']
            subprocess.Popen(cmd)
        else:
            print(f"Unsupported browser: {browser_name}")
            sys.exit(1)
    elif platform.system() == 'Windows':
        if browser_name == 'chrome':
            chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            cmd = [chrome_path, "--remote-debugging-port=9222"]
            subprocess.Popen(cmd)
            print("Chrome started with remote debugging on port 9222.")
        elif browser_name == 'firefox':
            firefox_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
            cmd = [firefox_path, "-start-debugger-server", "6000"]
            subprocess.Popen(cmd)
            print("Firefox started with remote debugging on port 6000.")
        else:
            print(f"Unsupported browser: {browser_name}")
            sys.exit(1)
    else:
        print("Unsupported operating system.")
        sys.exit(1)

def monitor_chrome_requests():
    import pychrome
    import threading
    import time
    import sys

    x_auth_token = None  # Initialize in the outer function scope

    # Connect to Chrome DevTools
    try:
        browser = pychrome.Browser(url="http://127.0.0.1:9222")

        # Open an existing tab or create a new one
        tabs = browser.list_tab()
        if not tabs:
            print("No active tabs found. Please open a page in Chrome.")
            sys.exit(1)
        tab = tabs[0]

        # Event to track if the auth token has been found
        auth_token_found = threading.Event()

        # Function to handle network requests
        def log_request(request, **kwargs):
            nonlocal x_auth_token  # Declare x_auth_token as nonlocal
            try:
                if request['url'] == 'https://api.gotinder.com/v2/profile/consents?locale=en':
                    print(f"Request to {request['url']} detected.")
                    headers = request.get('headers', {})
                    x_auth_token = headers.get('X-Auth-Token')
                    if x_auth_token:
                        print(f"X-Auth-Token found in request headers: {x_auth_token}")
                        auth_token_found.set()
                        return
            except Exception as e:
                print(f"Exception in log_request: {e}")

        # Function to handle network responses
        def log_response(response, **kwargs):
            nonlocal x_auth_token  # Declare x_auth_token as nonlocal
            try:
                if response['url'] == 'https://api.gotinder.com/v2/profile/consents?locale=en':
                    print(f"Response from {response['url']} detected.")
                    if response['status'] == 200:
                        print(f"Status code is 200 for {response['url']}.")
                        headers = response.get('headers', {})
                        x_auth_token = headers.get('X-Auth-Token')
                        if x_auth_token:
                            print(f"X-Auth-Token found in response headers: {x_auth_token}")
                            auth_token_found.set()
            except Exception as e:
                print(f"Exception in log_response: {e}")

        # Attach event handlers
        tab.Network.requestWillBeSent = log_request
        tab.Network.responseReceived = log_response

        # Start the tab and enable the Network domain
        tab.start()
        tab.Network.enable()

        print("Monitoring network requests in Chrome. Interact with the page, and watch the logs.")
        print("Press Ctrl+C to stop.")

        # Start a thread to monitor the auth_token_found event
        def wait_for_token():
            try:
                # Wait until the auth token is found or until interrupted
                while not auth_token_found.is_set():
                    time.sleep(0.5)
            except KeyboardInterrupt:
                print("Stopped by user.")

        monitor_thread = threading.Thread(target=wait_for_token, daemon=True)
        monitor_thread.start()

        # Let the function return without stopping the tab or disabling the Network domain
        return x_auth_token  # This will return None if the token hasn't been found yet

    except Exception as e:
        print(f"Error connecting to Chrome DevTools: {e}")
        sys.exit(1)

    # If no token is found
    return "X-Auth-Token not found. Reopen Chrome and try again"


def monitor_firefox_requests():
    print("Firefox debugging is not fully implemented in this script.")
    print("Consider using an alternative method or tool to monitor network requests in Firefox.")
    sys.exit(1)

def monitor_safari_requests():
    from selenium import webdriver

    print("Ensure that 'Allow Remote Automation' is enabled in Safari's Develop menu.")

    # Start Safari with safaridriver
    options = webdriver.SafariOptions()
    options.use_technology_preview = False  # Set to True if using Safari Technology Preview
    driver = webdriver.Safari(options=options)

    # Variable to track if the auth token has been found
    auth_token_found = False

    # Navigate to Tinder
    driver.get("https://tinder.com/")

    # Since Selenium does not provide network interception in Safari, we cannot directly monitor network requests
    print("Monitoring network requests in Safari using Selenium is not supported.")
    print("Consider using a proxy tool like mitmproxy to monitor network requests.")
    driver.quit()
    sys.exit(1)

if __name__ == "__main__":
    browser_choice = get_browser_choice()

    start_browser_with_debugging(browser_choice)
    # Wait a bit for the browser to start
    time.sleep(5)

    if browser_choice == 'chrome':
        token = monitor_chrome_requests()
        print(f"Returned Token: {token}")
    elif browser_choice == 'firefox':
        monitor_firefox_requests()
    elif browser_choice == 'safari':
        monitor_safari_requests()
    else:
        print(f"Unsupported browser: {browser_choice}")
        sys.exit(1)