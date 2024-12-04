import pychrome
import threading
import time
import os

# Disable proxies for local connections
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

def monitor_chrome_requests():

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