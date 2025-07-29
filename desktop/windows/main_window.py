
# windows/main_window.py - Simplified MainWindow
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import QTimer
import os

from UI.ui import Ui_MainWindow
# from core.fingerprint_capture import FingerprintScanner
from core.figerprint_capture import FingerprintScanner

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Configure fingerprint display
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
        
        # Initialize scanner
        self.scanner = FingerprintScanner(self.ui.fingerprintImageLabel)
        
        # Track preview state
        self.is_preview_active = False
        
        # Connect buttons
        self._connect_buttons()
        
        # Update button text
        self.ui.captureButton.setText("🎥 Start Preview")
        
        # Initially disable save button since we'll use main button for capture
        self.ui.saveCurrentFingerButton.setEnabled(False)
        
        print("✅ Application started successfully!")
    
    def _connect_buttons(self):
        """Connect UI buttons"""
        # Main capture button now toggles preview
        self.ui.captureButton.clicked.connect(self._toggle_preview)
        
        # Other buttons
        self.ui.saveCurrentFingerButton.clicked.connect(self._save_fingerprint)
        self.ui.nextFingerButton.clicked.connect(self._next_finger)
        self.ui.retakeCurrentButton.clicked.connect(self._retake_current)
    
    def _toggle_preview(self):
        """Toggle between start preview and capture image"""
        if not self.is_preview_active:
            # Start preview
            print("🎥 Starting preview...")
            success = self.scanner.start_preview()
            
            if success:
                self.is_preview_active = True
                self.ui.captureButton.setText("📷 Capture Image")
                self.ui.saveCurrentFingerButton.setEnabled(False)  # Disable separate save button
                
                # Update status
                self.ui.predictionResultBrowser.setHtml("""
                <p align="center" style="color: #10b981; font-weight: bold;">
                    📸 Live Preview Active<br>
                    <span style="color: #ffffff;">Position finger, then click 'Capture Image'</span>
                </p>
                """)
            else:
                QMessageBox.warning(self, "Scanner Error", 
                                  "Could not start scanner. Please check connection.")
        else:
            # Capture image and stop preview
            print("📷 Capturing and saving image...")
            filepath = self.scanner.capture_and_save_image()
            
            # Stop preview
            self.scanner.stop_preview()
            self.is_preview_active = False
            self.ui.captureButton.setText("🎥 Start Preview")
            self.ui.saveCurrentFingerButton.setEnabled(True)  # Re-enable save button
            
            if filepath:
                # Show success message
                QMessageBox.information(self, "Success", 
                                      f"Image captured and saved!\n\nFile: {os.path.basename(filepath)}")
                
                # Update status
                self.ui.predictionResultBrowser.setHtml(f"""
                <p align="center" style="color: #10b981; font-weight: bold;">
                    ✅ Image Captured & Saved!<br>
                    <span style="color: #ffffff;">File: {os.path.basename(filepath)}</span>
                </p>
                """)
            else:
                # Update status for failure
                self.ui.predictionResultBrowser.setHtml("""
                <p align="center" style="color: #ef4444; font-weight: bold;">
                    ❌ Capture Failed<br>
                    <span style="color: #ffffff;">Please try again</span>
                </p>
                """)
                QMessageBox.warning(self, "Error", "Failed to capture image!")
    
    def _save_fingerprint(self):
        """Save current fingerprint image"""
        if not self.is_preview_active:
            QMessageBox.information(self, "Info", "Please start preview first!")
            return
        
        print("💾 Saving fingerprint...")
        filepath = self.scanner.capture_and_save_image()
        
        if filepath:
            # Show success message
            QMessageBox.information(self, "Success", 
                                  f"Fingerprint saved successfully!\n\nFile: {os.path.basename(filepath)}")
            
            # Update status
            self.ui.predictionResultBrowser.setHtml(f"""
            <p align="center" style="color: #10b981; font-weight: bold;">
                💾 Image Saved Successfully!<br>
                <span style="color: #ffffff;">File: {os.path.basename(filepath)}</span>
            </p>
            """)
        else:
            QMessageBox.warning(self, "Error", "Failed to save image!")
    
    def _next_finger(self):
        """Move to next finger"""
        print("➡️ Next finger selected")
        # TODO: Implement finger selection logic
        QMessageBox.information(self, "Info", "Next finger selected (feature coming soon)")
    
    def _retake_current(self):
        """Retake current finger"""
        print("🔄 Retaking current finger")
        if self.is_preview_active:
            # Just continue with current preview
            QMessageBox.information(self, "Info", "Continue positioning finger for better capture")
        else:
            QMessageBox.information(self, "Info", "Please start preview first!")
    
    def closeEvent(self, event):
        """Clean up when closing"""
        print("🚪 Closing application...")
        if self.scanner:
            self.scanner.cleanup()
        event.accept()


