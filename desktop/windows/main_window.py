from PySide6.QtWidgets import QMainWindow, QMessageBox
from UI.ui import Ui_MainWindow
from core.fingerprint_controller import FingerprintCaptureController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.fingerprintImageLabel.setScaledContents(True)
        self.ui.fingerprintImageLabel.setStyleSheet("""
            QLabel {
                background-color: #1e293b;
                border: 2px solid #475569;
                border-radius: 8px;
                color: #94a3b8;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        self.capture_controller = FingerprintCaptureController(self.ui.fingerprintImageLabel)
        self.is_preview_active = False
        self._connect_buttons()
        self.ui.captureButton.setText("🎥 Start Preview")
        self.ui.saveCurrentFingerButton.setEnabled(False)

    def _connect_buttons(self):
        self.ui.captureButton.clicked.connect(self._toggle_preview)
        self.ui.saveCurrentFingerButton.clicked.connect(self._save_image)

    def _toggle_preview(self):
        if not self.is_preview_active:
            if self.capture_controller.start_preview():
                self.is_preview_active = True
                self.ui.captureButton.setText("📷 Capture Image")
                self.ui.saveCurrentFingerButton.setEnabled(False)
        else:
            filepath = self.capture_controller.capture_and_save_image()
            self.capture_controller.stop_preview()
            self.is_preview_active = False
            self.ui.captureButton.setText("🎥 Start Preview")
            self.ui.saveCurrentFingerButton.setEnabled(True)

            if filepath:
                QMessageBox.information(self, "Success", f"Image saved to: {filepath}")
            else:
                QMessageBox.warning(self, "Error", "Failed to capture image.")

    def _save_image(self):
        if not self.is_preview_active:
            QMessageBox.warning(self, "Warning", "Preview not active.")
            return
        filepath = self.capture_controller.capture_and_save_image()
        if filepath:
            QMessageBox.information(self, "Saved", f"Fingerprint saved to: {filepath}")

    def closeEvent(self, event):
        self.capture_controller.cleanup()
        event.accept()
