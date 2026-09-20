"""Floating Jarvis desktop interface."""

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QTextEdit, QVBoxLayout, QWidget
)

from jarvis.commands import handle_command, should_exit
from jarvis.speaker import speak
from jarvis.voice import listen


class ListenWorker(QThread):
    heard = Signal(str)
    status = Signal(str)

    def run(self):
        self.status.emit("LISTENING")
        text = listen()
        self.status.emit("READY")
        if text:
            self.heard.emit(text)


class JarvisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis")
        self.resize(520, 680)
        self.setMinimumSize(420, 560)

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)

        title = QLabel("JARVIS")
        title.setObjectName("title")
        subtitle = QLabel("Desktop Intelligence")
        subtitle.setObjectName("subtitle")
        self.status = QLabel("READY")
        self.status.setObjectName("status")

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setPlaceholderText("Your conversation will appear here...")

        row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a command...")
        self.input.returnPressed.connect(self.submit_text)
        send = QPushButton("Send")
        send.clicked.connect(self.submit_text)
        self.mic = QPushButton("Listen")
        self.mic.clicked.connect(self.start_listening)
        row.addWidget(self.input, 1)
        row.addWidget(send)
        row.addWidget(self.mic)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.status)
        layout.addWidget(self.chat, 1)
        layout.addLayout(row)
        self.setCentralWidget(root)

        self.setStyleSheet("""
            QMainWindow, QWidget { background: #080b12; color: #eaf6ff; }
            #title { font-size: 34px; font-weight: 700; letter-spacing: 7px; }
            #subtitle { color: #7d91a8; font-size: 13px; }
            #status {
                border: 1px solid #28465f; border-radius: 12px;
                padding: 10px; color: #8bdcff; font-weight: 700;
            }
            QTextEdit, QLineEdit {
                background: #0f1621; border: 1px solid #223448;
                border-radius: 14px; padding: 12px; font-size: 14px;
            }
            QPushButton {
                background: #14283a; border: 1px solid #315a78;
                border-radius: 12px; padding: 11px 16px; font-weight: 600;
            }
            QPushButton:hover { background: #1b3850; }
        """)

        self.worker = None
        self.append("Jarvis", "Ready. Type a command or press Listen.")

    def append(self, who: str, text: str):
        self.chat.append(f"<b>{who}</b><br>{text}<br>")

    def submit_text(self):
        text = self.input.text().strip()
        if text:
            self.input.clear()
            self.process(text)

    def start_listening(self):
        if self.worker and self.worker.isRunning():
            return
        self.worker = ListenWorker()
        self.worker.heard.connect(self.process)
        self.worker.status.connect(self.status.setText)
        self.worker.start()

    def process(self, text: str):
        self.append("You", text)
        if should_exit(text):
            self.append("Jarvis", "Goodbye.")
            speak("Goodbye.")
            QApplication.quit()
            return
        self.status.setText("THINKING")
        response = handle_command(text)
        self.append("Jarvis", response)
        self.status.setText("READY")
        speak(response)


def run_ui():
    app = QApplication.instance() or QApplication([])
    app.setApplicationName("Jarvis")
    window = JarvisWindow()
    window.show()
    app.exec()
