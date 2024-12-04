from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QWidget,
    QMessageBox,
)
import threading
from chrome_controller import ChromeController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SwipeMate Token Retriever")
        self.setGeometry(100, 100, 400, 300)

        # Layout
        layout = QVBoxLayout()

        # Instructions
        self.instructions = QLabel("Click the button below to open Chrome and retrieve your Tinder X-Auth-Token.")
        layout.addWidget(self.instructions)

        # Button to start Chrome
        self.start_button = QPushButton("Start Chrome")
        self.start_button.clicked.connect(self.start_chrome)
        layout.addWidget(self.start_button)

        # Display token
        self.token_label = QLabel("X-Auth-Token: ")
        layout.addWidget(self.token_label)

        # Input field for token (optional)
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Enter token manually (if needed)")
        layout.addWidget(self.token_input)

        # Button to send token to backend
        self.send_button = QPushButton("Send Token")
        self.send_button.clicked.connect(self.send_token)
        layout.addWidget(self.send_button)

        # Set the central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Chrome Controller
        self.chrome_controller = ChromeController()

    def start_chrome(self):
        """Start Chrome in debugging mode and retrieve the token."""
        self.instructions.setText("Starting Chrome... Please log into Tinder.")
        threading.Thread(target=self.retrieve_token).start()

    def retrieve_token(self):
        try:
            token = self.chrome_controller.start_and_get_token()
            self.token_label.setText(f"X-Auth-Token: {token}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def send_token(self):
        """Send token to backend."""
        token = self.token_input.text() or self.chrome_controller.token
        if not token:
            QMessageBox.warning(self, "Warning", "No token available to send.")
            return

        try:
            response = self.chrome_controller.send_token_to_backend(token)
            QMessageBox.information(self, "Success", f"Token sent successfully: {response}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))