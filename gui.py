import os
import sys
import uuid
from threading import Thread
from typing import Optional

import numpy as np
import sounddevice
import soundfile
import queue
import tempfile
import whisper
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QSizePolicy,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QGroupBox,
)

import main
from keychain_manager import get_openai_api_key_with_fallback

# Optional enhanced capabilities
try:
    from learning_system import (
        get_recent_activity,
        get_command_patterns,
    )
    LEARNING_TOOLS_AVAILABLE = True
except ImportError:
    LEARNING_TOOLS_AVAILABLE = False

try:
    from data_analysis import analyze_directory_structure
    DATA_ANALYSIS_AVAILABLE = True
except ImportError:
    DATA_ANALYSIS_AVAILABLE = False


def get_asset_path(path: str):
    return os.path.join(os.path.dirname(__file__), path)


RECORD_ICON_PATH = get_asset_path('assets/mic.svg')
STOP_ICON_PATH = get_asset_path('assets/stop.svg')


class MainWindow(QMainWindow):
    is_recording = False
    record_button: QPushButton
    ICON_LIGHT_THEME_BACKGROUND = '#333'
    ICON_DARK_THEME_BACKGROUND = '#DDD'
    recording_thread: Optional[Thread] = None
    transcription_thread: Optional[Thread] = None
    temp_file_path: Optional[str] = None

    def __init__(self):
        super().__init__(flags=Qt.WindowType.Window)

        self.samples_buffer = np.ndarray([], dtype=np.float32)
        self.audio_queue = queue.Queue()
        self.current_command: Optional[str] = None

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setMinimumSize(560, 580)
        self.setWindowTitle("Atom AI Assistant")

        widget = QWidget(parent=self)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(14)

        # Title
        title_label = QLabel("Atom AI Assistant", parent=self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 22px; font-weight: 600;")
        main_layout.addWidget(title_label)

        # Controls section
        controls_box = QGroupBox("Voice Control", parent=self)
        controls_layout = QVBoxLayout()

        self.record_icon = self.load_icon(RECORD_ICON_PATH)
        self.stop_icon = self.load_icon(STOP_ICON_PATH)

        self.record_button = QPushButton(self.load_icon(RECORD_ICON_PATH), "Record", parent=self)
        self.record_button.clicked.connect(self.on_button_clicked)
        self.record_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.record_button.setMinimumHeight(56)
        window_color = self.palette().window().color()
        background_color = window_color.lighter(150) if self.is_dark_theme() else window_color.darker(150)
        self.record_button.setStyleSheet(
            "QPushButton { border-radius: 10px; font-size: 17px; background-color: %s; padding: 12px; }" % background_color.name())

        self.transcription_label = QLabel("Click 'Record' to begin", parent=self)
        self.transcription_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.transcription_label.setWordWrap(True)
        self.transcription_label.setStyleSheet("font-size: 14px;")

        controls_layout.addWidget(self.record_button)
        controls_layout.addWidget(self.transcription_label)
        controls_box.setLayout(controls_layout)
        main_layout.addWidget(controls_box)

        # Manual command entry
        command_box = QGroupBox("Type a Command", parent=self)
        command_layout = QHBoxLayout()
        self.command_input = QLineEdit(parent=self)
        self.command_input.setPlaceholderText("Ask Atom to do something... (e.g., 'Organize my Downloads folder')")
        self.command_input.returnPressed.connect(self.on_run_command)

        self.run_command_button = QPushButton("Run", parent=self)
        self.run_command_button.clicked.connect(self.on_run_command)
        self.run_command_button.setMinimumWidth(90)

        command_layout.addWidget(self.command_input)
        command_layout.addWidget(self.run_command_button)
        command_box.setLayout(command_layout)
        main_layout.addWidget(command_box)

        # Status + log section
        status_box = QGroupBox("Activity", parent=self)
        status_layout = QVBoxLayout()

        self.status_label = QLabel("Ready for your command.", parent=self)
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("font-size: 13px;")

        self.log_view = QTextEdit(parent=self)
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet("font-family: 'SF Mono', monospace; font-size: 12px;")
        self.log_view.setMinimumHeight(160)

        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.log_view)
        status_box.setLayout(status_layout)
        main_layout.addWidget(status_box)

        # Insights section
        insights_box = QGroupBox("Atom Insights", parent=self)
        insights_layout = QVBoxLayout()
        self.insights_view = QTextEdit(parent=self)
        self.insights_view.setReadOnly(True)
        self.insights_view.setPlaceholderText("Atom will show recent activity, learned preferences, and suggestions here.")
        self.insights_view.setStyleSheet("font-family: 'SF Mono', monospace; font-size: 12px;")
        self.insights_view.setMinimumHeight(150)

        insights_layout.addWidget(self.insights_view)
        insights_box.setLayout(insights_layout)
        main_layout.addWidget(insights_box)

        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        self.append_log("✅ Atom is ready.")
        self.refresh_insights()

        # Periodically refresh insights to keep information up-to-date
        self.insights_timer = QTimer(self)
        self.insights_timer.timeout.connect(self.refresh_insights)
        self.insights_timer.start(90_000)  # every 90 seconds

    def transcribe_recording(self):
        model = whisper.load_model("base")
        result = model.transcribe(audio=self.temp_file_path, language="en", task="transcribe")

        text = result["text"]
        print(f'Transcribed text: {text}')

        if text is None:
            self.transcription_label.setText('No text found. Please try again.')
        else:
            self.transcription_label.setText(f'"{text.strip()}"')

            try:
                # Run command execution
                main.main(result["text"])
            except Exception as e:
                print(f'Error executing command: {e}')
                self.transcription_label.setText(f'An error occurred: {str(e)}')

        self.record_button.setDisabled(False)

    def start_recording(self):
        device = sounddevice.query_devices(kind='input')

        self.temp_file_path = os.path.join(tempfile.gettempdir(), f'{uuid.uuid1()}.wav')
        print(f'Temporary recording path: {self.temp_file_path}')

        with soundfile.SoundFile(self.temp_file_path, mode='x', samplerate=int(device['default_samplerate']),
                                 channels=1) as file:
            with sounddevice.InputStream(channels=1, callback=self.callback, device=device['index'], dtype="float32"):
                while self.is_recording:
                    file.write(self.queue.get())

    def callback(self, in_data, frames, time, status):
        self.queue.put(in_data.copy())

    def on_button_clicked(self):
        if self.is_recording:
            self.record_button.setText("Record")
            self.record_button.setIcon(self.record_icon)
            self.is_recording = False

            self.transcription_label.setText('Transcribing...')
            self.record_button.setDisabled(True)

            self.transcription_thread = Thread(target=self.transcribe_recording)
            self.transcription_thread.start()
        else:
            # Reset samples buffer
            self.samples_buffer = np.ndarray([], dtype=np.float32)

            self.recording_thread = Thread(target=self.start_recording)
            self.recording_thread.start()

            self.transcription_label.setText('Listening...')

            self.record_button.setText("Stop")
            self.record_button.setIcon(self.stop_icon)
            self.is_recording = True

    def is_dark_theme(self):
        return self.palette().window().color().black() > 127

    def load_icon(self, file_path: str):
        background = self.ICON_DARK_THEME_BACKGROUND if self.is_dark_theme() else self.ICON_LIGHT_THEME_BACKGROUND
        return self.load_icon_with_color(file_path, background)

    @staticmethod
    def load_icon_with_color(file_path: str, color: str):
        """Adapted from https://stackoverflow.com/questions/15123544/change-the-color-of-an-svg-in-qt"""
        pixmap = QPixmap(file_path)
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), QColor(color))
        painter.end()
        return QIcon(pixmap)


class Application(QApplication):
    window: MainWindow

    def __init__(self) -> None:
        super().__init__(sys.argv)

        self.window = MainWindow()
        self.window.show()


if __name__ == "__main__":
    # Check API key availability before starting GUI
    api_key = get_openai_api_key_with_fallback()
    if not api_key:
        print("\n❌ No OpenAI API key found!")
        print("Please set up your API key first by running:")
        print("python keychain_manager.py")
        sys.exit(1)
    
    app = Application()
    sys.exit(app.exec())
