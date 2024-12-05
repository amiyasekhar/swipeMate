import sys
import platform  # Detect OS
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QMessageBox, QPushButton
import threading
import time
import requests  # For backend requests
import webbrowser  # To open the checkout session URL
import os
# Import necessary helper functions
from find_chrome import find_chrome_binary
from install_chrome import install_chrome_linux, install_chrome_macos, install_chrome_windows
from monitor_chrome import monitor_chrome_requests
from run_chrome import start_browser_with_debugging

print("Environment Variables:")
for key, value in os.environ.items():
    print(f"{key}={value}")
print("Current Working Directory:", os.getcwd())

if getattr(sys, 'frozen', False):
    # The application is frozen (bundled by py2app)
    application_path = os.path.dirname(sys.executable)
    print("Application path", application_path)
else:
    # The application is running in a normal Python environment
    application_path = os.path.dirname(os.path.abspath(__file__))
    print("Application path", application_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SwipeMate Token Retriever")
        self.setGeometry(100, 100, 800, 600)

        # Initialize token variable
        self.token = None

        # UI Setup
        layout = QVBoxLayout()
        self.token_label = QLabel("Fetching X-Auth-Token...")
        layout.addWidget(self.token_label)

        # Copy Token Button
        self.copy_button = QPushButton("Copy Token")
        self.copy_button.setEnabled(False)  # Disabled initially
        self.copy_button.clicked.connect(self.copy_token)
        layout.addWidget(self.copy_button)

        # Create Checkout Session Button
        self.checkout_button = QPushButton("Create Checkout Session")
        self.checkout_button.setEnabled(False)  # Disabled initially
        self.checkout_button.clicked.connect(self.create_checkout_session)
        layout.addWidget(self.checkout_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Automatically start token retrieval
        self.retrieve_token()

    def retrieve_token(self):
        threading.Thread(target=self._retrieve_token_worker).start()

    def _retrieve_token_worker(self):
        try:
            # Step 1: Find or Install Chrome
            chrome_path = find_chrome_binary()
            if not chrome_path:
                current_os = platform.system()
                self.update_status("Chrome not found. Attempting installation...")
                if current_os == "Linux":
                    install_chrome_linux()
                elif current_os == "Darwin":
                    install_chrome_macos()
                elif current_os == "Windows":
                    install_chrome_windows()
                else:
                    raise Exception(f"Unsupported OS: {current_os}")
                chrome_path = find_chrome_binary()
                if not chrome_path:
                    raise Exception("Failed to locate or install Chrome.")

            # Step 2: Start Chrome with Debugging
            self.update_status("Starting Chrome and monitoring for token...")
            start_browser_with_debugging("chrome")
            time.sleep(10)

            # Step 3: Monitor Chrome for X-Auth-Token
            self.update_status("Monitoring Chrome for token...")
            token = monitor_chrome_requests()
            if token:
                self.token = token  # Store the token
                self.update_status(f"Token Found: {token}")
                self.copy_button.setEnabled(True)  # Enable buttons
                self.checkout_button.setEnabled(True)
            else:
                self.update_status("Token not found.")
        except Exception as e:
            self.update_status(f"Error: {str(e)}")

    def copy_token(self):
        """Copy the token to the clipboard."""
        if self.token:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.token)
            QMessageBox.information(self, "Token Copied", "The token has been copied to the clipboard!")
        else:
            QMessageBox.warning(self, "No Token", "No token available to copy.")

    def create_checkout_session(self):
        """Create a Stripe Checkout session."""
        if self.token:
            try:
                # List of backend URLs to try
                backend_urls = [
                    "https://swipemate.onrender.com/create-checkout-session",
                    "http://localhost:3002/create-checkout-session"
                ]

                session_url = None
                for backend_url in backend_urls:
                    try:
                        # Make a POST request to the backend with the token
                        response = requests.post(backend_url, json={"authToken": self.token}, timeout=5)
                        response_data = response.json()

                        if response.status_code == 200 and "url" in response_data:
                            session_url = response_data["url"]
                            print(f"Backend url: {backend_url}")
                            break  # Stop trying once a valid session URL is found
                        else:
                            print(f"Failed to create session with {backend_url}: {response_data.get('error', 'Unknown error')}")
                    except requests.exceptions.RequestException as e:
                        print(f"Error connecting to {backend_url}: {str(e)}")
                
                if session_url:
                    # Open the URL in the default browser
                    webbrowser.open(session_url)
                    QMessageBox.information(self, "Checkout Session", "Checkout session created and opened in your browser!")
                else:
                    QMessageBox.warning(self, "Error", "Failed to create a checkout session with any backend URL.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
        else:
            QMessageBox.warning(self, "No Token", "No token available to create a checkout session.")

    def update_status(self, message):
        """Update the token_label text in the main thread."""
        self.token_label.setText(message)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()