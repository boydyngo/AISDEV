import os
import time
import tempfile
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, 
    QLabel, QComboBox, QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSlot, QThread, pyqtSignal, QObject
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl

# Worker thread for API calls
class TTSWorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(str, int)  # audio_file_path, actual_tokens
    progress = pyqtSignal(int)  # For progress bar

class TTSWorker(QObject):
    def __init__(self, ai_service, text, voice, speed):
        super().__init__()
        self.ai_service = ai_service
        self.text = text
        self.voice = voice
        self.speed = speed
        self.signals = TTSWorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            self.signals.progress.emit(10)  # Starting progress
            audio_file_path, actual_tokens = self.ai_service.synthesize_speech(
                self.text, self.voice, self.speed
            )
            self.signals.progress.emit(90)  # Almost done
            
            if audio_file_path:
                self.signals.result.emit(audio_file_path, actual_tokens)
            else:
                self.signals.error.emit("Failed to generate audio file.")
                
            self.signals.progress.emit(100)  # Complete
        except Exception as e:
            self.signals.error.emit(f"TTS Error: {e}")
        finally:
            self.signals.finished.emit()

# TTS Module Widget
class TTSModule(QWidget):
    def __init__(self, ai_service, parent=None):
        super().__init__(parent)
        self.ai_service = ai_service
        self.current_text = ""
        self.audio_file_path = None
        
        # Media player setup
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        
        # Thread management
        self.worker_thread = None
        self.worker = None
        
        self._init_ui()
        self._connect_signals()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # Playback controls
        controls_layout = QHBoxLayout()
        
        self.play_pause_button = QPushButton("Play")
        self.play_pause_button.setCheckable(True)
        
        self.stop_button = QPushButton("Stop")
        
        self.skip_back_button = QPushButton("<<10s")
        self.skip_forward_button = QPushButton("10s>>")
        
        controls_layout.addWidget(self.play_pause_button)
        controls_layout.addWidget(self.stop_button)
        controls_layout.addWidget(self.skip_back_button)
        controls_layout.addWidget(self.skip_forward_button)
        
        layout.addLayout(controls_layout)
        
        # Speed control
        speed_layout = QVBoxLayout()
        self.speed_label = QLabel("Speed: 1.0x")
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(5)  # 0.5x
        self.speed_slider.setMaximum(20)  # 2.0x
        self.speed_slider.setValue(10)  # 1.0x default
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        
        speed_layout.addWidget(self.speed_label)
        speed_layout.addWidget(self.speed_slider)
        
        layout.addLayout(speed_layout)
        
        # Volume control
        volume_layout = QVBoxLayout()
        self.volume_label = QLabel("Volume: 100%")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)  # 100% default
        self.audio_output.setVolume(1.0)
        
        volume_layout.addWidget(self.volume_label)
        volume_layout.addWidget(self.volume_slider)
        
        layout.addLayout(volume_layout)
        
        # Voice selection
        voice_layout = QVBoxLayout()
        self.voice_label = QLabel("Voice:")
        self.voice_combo = QComboBox()
        self.voice_combo.addItems(["Default Male", "Default Female", "UK Male"])
        
        voice_layout.addWidget(self.voice_label)
        voice_layout.addWidget(self.voice_combo)
        
        layout.addLayout(voice_layout)
        
        # Status and progress
        self.token_label = QLabel("Est. Tokens: 0")
        self.status_label = QLabel("Ready")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        layout.addWidget(self.token_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
        self._update_button_states()  # Initial state
    
    def _connect_signals(self):
        # Button connections
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.stop_button.clicked.connect(self.stop_playback)
        self.skip_back_button.clicked.connect(lambda: self.handle_skip(-10))
        self.skip_forward_button.clicked.connect(lambda: self.handle_skip(10))
        
        # Slider connections
        self.speed_slider.valueChanged.connect(self.update_speed_label)
        self.volume_slider.valueChanged.connect(self.update_volume)
        
        # Combo box connections
        self.voice_combo.currentTextChanged.connect(self.voice_changed)
        
        # Media player connections
        self.player.mediaStatusChanged.connect(self.media_status_changed)
        self.player.errorOccurred.connect(self.player_error)
    
    def set_text(self, text):
        if text != self.current_text:
            self.current_text = text
            self.stop_playback()  # Stop if playing different text
            self.estimate_tokens()  # Estimate cost for new text
            self._update_button_states()
    
    def estimate_tokens(self):
        if self.current_text:
            try:
                estimated_tokens = self.ai_service.estimate_tts_tokens(
                    self.current_text, 
                    self.voice_combo.currentText()
                )
                self.token_label.setText(f"Est. Tokens: {estimated_tokens}")
            except Exception as e:
                self.token_label.setText("Est. Tokens: Error")
                print(f"Token estimation error: {e}")
        else:
            self.token_label.setText("Est. Tokens: 0")
    
    @pyqtSlot(bool)
    def toggle_play_pause(self, checked):
        if checked:  # Play button pressed
            if self.player.mediaStatus() == QMediaPlayer.MediaStatus.PausedMedia:
                self.player.play()
                self.status_label.setText("Playing...")
            elif self.audio_file_path and self.player.mediaStatus() != QMediaPlayer.MediaStatus.LoadingMedia:
                # If we already have the file, just play it
                source = QUrl.fromLocalFile(self.audio_file_path)
                self.player.setSource(source)
                self.player.play()
                self.status_label.setText("Playing...")
            else:
                # Need to synthesize first
                self.synthesize_and_play()
        else:  # Pause button pressed
            if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
                self.player.pause()
                self.status_label.setText("Paused")
    
    @pyqtSlot()
    def stop_playback(self):
        self.player.stop()
        self.status_label.setText("Stopped")
        self.play_pause_button.setChecked(False)
        self._update_button_states()
    
    def handle_skip(self, seconds):
        if self.player.playbackState() != QMediaPlayer.PlaybackState.StoppedState:
            current_position = self.player.position()
            new_position = max(0, current_position + seconds * 1000)  # Convert to milliseconds
            self.player.setPosition(new_position)
    
    def synthesize_and_play(self):
        if not self.current_text:
            QMessageBox.warning(self, "Warning", "No text to synthesize.")
            self.play_pause_button.setChecked(False)
            return
        
        # Token cost confirmation for large texts
        estimated_tokens = self.ai_service.estimate_tts_tokens(
            self.current_text, 
            self.voice_combo.currentText()
        )
        
        if estimated_tokens > 1000:  # Example threshold
            reply = QMessageBox.question(
                self, 
                "Confirm Cost",
                f"This operation is estimated to cost {estimated_tokens} tokens. Proceed?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                self.play_pause_button.setChecked(False)
                return
        
        # Start synthesis
        self.status_label.setText("Synthesizing...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.play_pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        
        # Create worker thread
        self.worker_thread = QThread()
        self.worker = TTSWorker(
            self.ai_service,
            self.current_text,
            self.voice_combo.currentText(),
            self.speed_slider.value() / 10.0
        )
        self.worker.moveToThread(self.worker_thread)
        
        # Connect signals
        self.worker.signals.result.connect(self.on_synthesis_success)
        self.worker.signals.error.connect(self.on_synthesis_error)
        self.worker.signals.finished.connect(self.on_synthesis_finished)
        self.worker.signals.progress.connect(self.progress_bar.setValue)
        
        # Start thread
        self.worker_thread.started.connect(self.worker.run)
        self.worker.signals.finished.connect(self.worker_thread.quit)
        self.worker.signals.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        
        self.worker_thread.start()
    
    @pyqtSlot(str, int)
    def on_synthesis_success(self, audio_file_path, actual_tokens):
        self.audio_file_path = audio_file_path
        self.status_label.setText(f"Synthesis complete. Tokens: {actual_tokens}")
        self.token_label.setText(f"Est. Tokens: {actual_tokens}")  # Update with actual
        
        # Set up player with the new audio file
        source = QUrl.fromLocalFile(self.audio_file_path)
        self.player.setSource(source)
        
        if self.play_pause_button.isChecked():  # If user still wants to play
            self.player.play()
            self.status_label.setText("Playing...")
        else:
            self.status_label.setText("Ready to play.")
    
    @pyqtSlot(str)
    def on_synthesis_error(self, error_msg):
        QMessageBox.critical(self, "Synthesis Error", error_msg)
        self.status_label.setText("Error")
        self.play_pause_button.setChecked(False)
    
    @pyqtSlot()
    def on_synthesis_finished(self):
        self.progress_bar.setVisible(False)
        self.worker_thread = None
        self.worker = None
        self._update_button_states()
    
    @pyqtSlot(QMediaPlayer.MediaStatus)
    def media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            self._update_button_states()
        elif status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.status_label.setText("Finished")
            self.play_pause_button.setChecked(False)
            self.player.setSource(QUrl())  # Clear source
            self._update_button_states()
        elif status == QMediaPlayer.MediaStatus.InvalidMedia:
            self.status_label.setText("Error: Invalid audio")
            self.play_pause_button.setChecked(False)
            QMessageBox.warning(self, "Playback Error", "Could not load or play the audio file.")
            self.audio_file_path = None
    
    @pyqtSlot()
    def player_error(self):
        self.status_label.setText(f"Player Error: {self.player.errorString()}")
        self.play_pause_button.setChecked(False)
        QMessageBox.warning(self, "Playback Error", f"Error playing audio: {self.player.errorString()}")
        self.audio_file_path = None
    
    @pyqtSlot(int)
    def update_speed_label(self, value):
        speed = value / 10.0
        self.speed_label.setText(f"Speed: {speed:.1f}x")
        
        # Stop playback if speed changes - requires re-synthesis
        self.stop_playback()
        self.estimate_tokens()
    
    @pyqtSlot(int)
    def update_volume(self, value):
        volume = value / 100.0
        self.audio_output.setVolume(volume)
        self.volume_label.setText(f"Volume: {value}%")
    
    @pyqtSlot(str)
    def voice_changed(self, voice_name):
        # Stop playback if voice changes - requires re-synthesis
        self.stop_playback()
        self.estimate_tokens()
    
    def _update_button_states(self):
        can_play = bool(self.current_text) or bool(self.audio_file_path)
        is_synthesizing = self.worker_thread is not None and self.worker_thread.isRunning()
        is_playing = self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState
        
        self.play_pause_button.setEnabled(can_play and not is_synthesizing)
        self.stop_button.setEnabled((is_playing or self.player.playbackState() == QMediaPlayer.PlaybackState.PausedState) and not is_synthesizing)
        self.skip_back_button.setEnabled(is_playing or self.player.playbackState() == QMediaPlayer.PlaybackState.PausedState)
        self.skip_forward_button.setEnabled(is_playing or self.player.playbackState() == QMediaPlayer.PlaybackState.PausedState)
    
    def cleanup(self):
        """Clean up temporary files when closing"""
        self.stop_playback()
        
        if self.audio_file_path and os.path.exists(self.audio_file_path):
            try:
                if "temp" in self.audio_file_path.lower() or os.path.dirname(self.audio_file_path) == tempfile.gettempdir():
                    os.remove(self.audio_file_path)
                    print(f"Removed temp file: {self.audio_file_path}")
            except Exception as e:
                print(f"Error removing temp file {self.audio_file_path}: {e}")