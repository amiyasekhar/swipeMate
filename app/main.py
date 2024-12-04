import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow

# Define your main application window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SwipeMate")
        self.setGeometry(100, 100, 800, 600)  # Example geometry, adjust as needed

# Function to launch Chrome (on main thread after the UI loads)
def launch_chrome():
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    subprocess.Popen([chrome_path, "--remote-debugging-port=9222"])

# Main application function
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Launch Chrome after initializing the UI
    launch_chrome()

    sys.exit(app.exec())

# Ensure the code runs only when executed directly
if __name__ == "__main__":
    main()