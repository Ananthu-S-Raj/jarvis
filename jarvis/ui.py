"""Pet-style Jarvis UI with always-on listening."""

from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QTextEdit, QVBoxLayout, QWidget
)

from jarvis.commands import handle_command, should_exit
from jarvis.speaker import speak
from jarvis.voice import listen


class ListenWorker(QThread):
    heard = Signal(str)
    finished_cycle = Signal()

    def run(self):
        text = listen()
        if text:
            self.heard.emit(text)
        self.finished_cycle.emit()


class JarvisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis")
        self.resize(500, 640)
        self.setMinimumSize(420, 540)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.listening_enabled = True
        self.worker = None

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        top = QHBoxLayout()
        title = QLabel("JARVIS")
        title.setObjectName("title")
        self.status = QLabel("LISTENING")
        self.status.setObjectName("status")
        top.addWidget(title)
        top.addStretch()
        top.addWidget(self.status)

        subtitle = QLabel("Desktop companion")
        subtitle.setObjectName("subtitle")

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a command...")
        self.input.returnPressed.connect(self.submit_text)
        send = QPushButton("Send")
        send.clicked.connect(self.submit_text)
        self.mic = QPushButton("Pause listening")
        self.mic.clicked.connect(self.toggle_listening)
        row.addWidget(self.input, 1)
        row.addWidget(send)
        row.addWidget(self.mic)

        layout.addLayout(top)
        layout.addWidget(subtitle)
        layout.addWidget(self.chat, 1)
        layout.addLayout(row)
        self.setCentralWidget(root)

        self.setStyleSheet("""
            QMainWindow, QWidget { background: #080b12; color: #eaf6ff; }
            #title { font-size: 30px; font-weight: 700; letter-spacing: 6px; }
            #subtitle { color: #71869b; font-size: 13px; }
            #status {
                border: 1px solid #28465f; border-radius: 11px;
                padding: 8px 12px; color: #8bdcff; font-weight: 700;
            }
            QTextEdit, QLineEdit {
                background: #0f1621; border: 1px solid #223448;
                border-radius: 14px; padding: 12px; font-size: 14px;
            }
            QPushButton {
                background: #14283a; border: 1px solid #315a78;
                border-radius: 12px; padding: 11px 14px; font-weight: 600;
            }
            QPushButton:hover { background: #1b3850; }
        """)

        self.append("Jarvis", "I'm listening.")
        QTimer.singleShot(350, self.start_listening)

    def append(self, who, text):
        self.chat.append(f"<b>{who}</b><br>{text}<br>")

    def submit_text(self):
        text = self.input.text().strip()
        if text:
            self.input.clear()
            self.process(text, spoken=False)

    def toggle_listening(self):
        self.listening_enabled = not self.listening_enabled
        self.mic.setText("Pause listening" if self.listening_enabled else "Resume listening")
        self.status.setText("LISTENING" if self.listening_enabled else "PAUSED")
        if self.listening_enabled:
            self.start_listening()

    def start_listening(self):
        if not self.listening_enabled:
            return
        if self.worker and self.worker.isRunning():
            return
        self.status.setText("LISTENING")
        self.worker = ListenWorker()
        self.worker.heard.connect(lambda text: self.process(text, spoken=True))
        self.worker.finished_cycle.connect(self.restart_listening)
        self.worker.start()

    def restart_listening(self):
        if self.listening_enabled:
            QTimer.singleShot(200, self.start_listening)

    def process(self, text, spoken=False):
        self.append("You", text)
        if should_exit(text):
            self.append("Jarvis", "Goodbye.")
            QApplication.quit()
            return
        self.status.setText("THINKING")
        response = handle_command(text)
        self.append("Jarvis", response)
        # Voice responses are reserved for voice interaction. Typed chat stays quiet.
        if spoken:
            speak(response)
        self.status.setText("LISTENING" if self.listening_enabled else "READY")

    def changeEvent(self, event):
        # Minimized = pet mode: keep working, but hide the large interface.
        if event.type() == event.Type.WindowStateChange and self.isMinimized():
            QTimer.singleShot(0, self.hide)
        super().changeEvent(event)


def run_ui():
    app = QApplication.instance() or QApplication([])
    app.setApplicationName("Jarvis")
    app.setQuitOnLastWindowClosed(False)
    window = JarvisWindow()
    window.showMaximized()
    app.exec()
