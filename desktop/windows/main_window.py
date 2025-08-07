import sys
import os
import uuid
import json
import cv2
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QMainWindow, QMessageBox, QApplication
from UI.ui import Ui_MainWindow
from core.fingerprint_controller import FingerprintCaptureController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize UI elements
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

        # Fingerprint capture controller
        self.capture_controller = FingerprintCaptureController(self.ui.fingerprintImageLabel)
        self.is_preview_active = False
        self.current_captured_image = None
        self.current_pattern = None
        self.patient_uuid = None
        self.captured_fingers = {}

        # Finger order for workflow
        self.finger_order = [
            "Right Thumb", "Right Index Finger", "Right Middle Finger", "Right Ring Finger", "Right Little Finger",
            "Left Thumb", "Left Index Finger", "Left Middle Finger", "Left Ring Finger", "Left Little Finger"
        ]
        self.current_finger_index = 0

        # Connect signals and initialize UI
        self._connect_signals()
        self._initialize_ui()

    def _connect_signals(self):
        """Connect all UI signals to their handlers."""
        self.ui.captureButton.clicked.connect(self._toggle_preview)
        self.ui.saveCurrentFingerButton.clicked.connect(self._save_current_finger)
        self.ui.nextFingerButton.clicked.connect(self._on_next_finger)
        self.ui.retakeCurrentButton.clicked.connect(self._on_retake_current)
        self.ui.saveAllDataButton.clicked.connect(self._on_save_all_data)
        self.ui.clearAllDataButton.clicked.connect(self._on_clear_all_data)
        self.ui.agreeButton.clicked.connect(self._on_agree)
        self.ui.disagreeButton.clicked.connect(self._on_disagree)
        self.ui.fingerprintPatternComboBox.currentIndexChanged.connect(self._on_pattern_selected)
        self.ui.pushButton.clicked.connect(lambda: QMessageBox.information(self, "Info", "Collect Data feature not available yet."))
        self.ui.pushButton_2.clicked.connect(lambda: QMessageBox.information(self, "Info", "Edit Data feature not available yet."))

        # Form validation signals
        self.ui.nameLineEdit.textChanged.connect(self._update_button_states)
        self.ui.ageLineEdit.textChanged.connect(self._update_button_states)
        self.ui.genderComboBox.currentIndexChanged.connect(self._update_button_states)
        self.ui.groupComboBox.currentIndexChanged.connect(self._update_button_states)
        self.ui.smokingComboBox.currentIndexChanged.connect(self._update_button_states)
        self.ui.dentalDiseaseCheckBox.stateChanged.connect(self._on_dental_disease_checked)
        self.ui.dentalDiseaseCheckBox.stateChanged.connect(self._update_button_states)
        self.ui.dentalDiseaseTypeLineEdit.textChanged.connect(self._update_button_states)

    def _initialize_ui(self):
        """Set initial UI state."""
        self.ui.dentalDiseaseTypeLineEdit.setEnabled(False)
        self.ui.predictionResultBrowser.setVisible(False)
        self.ui.agreeButton.setVisible(False)
        self.ui.disagreeButton.setVisible(False)
        self.ui.manualPatternWidget.setVisible(False)
        self.ui.saveCurrentFingerButton.setEnabled(False)
        self.ui.nextFingerButton.setEnabled(False)
        self.ui.retakeCurrentButton.setEnabled(False)
        self.ui.captureButton.setText("🎥 Start Preview")
        self._update_finger_selection()
        self._update_captured_summary()

    def _on_dental_disease_checked(self, state):
        """Enable/disable dental condition field based on checkbox."""
        self.ui.dentalDiseaseTypeLineEdit.setEnabled(state == Qt.Checked)

    def _validate_form(self):
        """Validate all required patient information fields."""
        name = self.ui.nameLineEdit.text().strip()
        age_text = self.ui.ageLineEdit.text().strip()
        gender_index = self.ui.genderComboBox.currentIndex()
        group_index = self.ui.groupComboBox.currentIndex()
        smoking_index = self.ui.smokingComboBox.currentIndex()

        if not name:
            return False
        try:
            age = int(age_text)
            if age <= 0 or age > 120:
                return False
        except ValueError:
            return False
        if gender_index == 0 or group_index == 0 or smoking_index == 0:
            return False
        if self.ui.dentalDiseaseCheckBox.isChecked() and not self.ui.dentalDiseaseTypeLineEdit.text().strip():
            return False
        return True

    def _update_button_states(self):
        """Update button states based on form validity and fingerprint progress."""
        is_form_valid = self._validate_form()
        all_fingers_captured = len(self.captured_fingers) == 10
        self.ui.captureButton.setEnabled(is_form_valid)
        self.ui.saveAllDataButton.setEnabled(is_form_valid and all_fingers_captured)

    def _toggle_preview(self):
        """Toggle between preview and capture modes."""
        if not self.is_preview_active:
            if self.capture_controller.start_preview():
                self.is_preview_active = True
                self.ui.captureButton.setText("📷 Capture Image")
                # Hide prediction UI during preview
                self.ui.predictionResultBrowser.setVisible(False)
                self.ui.agreeButton.setVisible(False)
                self.ui.disagreeButton.setVisible(False)
                self.ui.manualPatternWidget.setVisible(False)
        else:
            if not self._validate_form():
                QMessageBox.warning(self, "Form Incomplete", "Please complete all required patient information before capturing fingerprints.")
                return
            self.capture_controller.stop_preview()
            self.is_preview_active = False
            self.ui.captureButton.setText("🎥 Start Preview")
            self.current_captured_image = self.capture_controller.current_image
            if self.current_captured_image is not None:
                # Simulate AI prediction
                predicted_pattern = "Plain Arch"
                self.current_pattern = predicted_pattern
                self.ui.predictionResultBrowser.setHtml(f"""
                    <p align="center"><span style="font-size:12pt; font-weight:700; color:#ffffff;">🤖 AI Model Prediction: {predicted_pattern}</span></p>
                    <p align="center"><span style="font-size:11pt; color:#d1d5db;">Do you agree with the AI prediction?</span></p>
                """)
                self.ui.predictionResultBrowser.setVisible(True)
                self.ui.agreeButton.setVisible(True)
                self.ui.disagreeButton.setVisible(True)
                self.ui.manualPatternWidget.setVisible(False)
                self.ui.saveCurrentFingerButton.setEnabled(False)
            else:
                QMessageBox.warning(self, "Error", "Failed to capture image.")

    def _on_agree(self):
        """Handle agreement with AI prediction."""
        self.ui.agreeButton.setVisible(False)
        self.ui.disagreeButton.setVisible(False)
        self.ui.manualPatternWidget.setVisible(False)
        self.ui.saveCurrentFingerButton.setEnabled(True)

    def _on_disagree(self):
        """Handle disagreement with AI prediction, show pattern selection."""
        self.ui.manualPatternWidget.setVisible(True)
        self.ui.fingerprintPatternComboBox.setCurrentIndex(0)
        self.ui.saveCurrentFingerButton.setEnabled(False)

    def _on_pattern_selected(self, index):
        """Handle manual pattern selection."""
        if index > 0:
            self.current_pattern = self.ui.fingerprintPatternComboBox.currentText()
            self.ui.saveCurrentFingerButton.setEnabled(True)

    def _save_current_finger(self):
        """Save the captured fingerprint for the current finger."""
        finger = self.ui.fingerSelectionComboBox.currentText()
        if finger == "Select finger to capture":
            QMessageBox.warning(self, "Warning", "Please select a finger to capture.")
            return
        if finger in self.captured_fingers:
            QMessageBox.warning(self, "Warning", f"{finger} has already been captured. Use 'Retake' if needed.")
            return
        if self.current_captured_image is None:
            QMessageBox.warning(self, "Warning", "No image captured.")
            return
        if not self.current_pattern:
            QMessageBox.warning(self, "Warning", "Please select a pattern.")
            return

        # Generate UUID and folder on first save
        if self.patient_uuid is None:
            self.patient_uuid = str(uuid.uuid4())
            os.makedirs(os.path.join("data", self.patient_uuid), exist_ok=True)

        # Save fingerprint image
        safe_pattern = self.current_pattern.replace("/", "_").replace("\\", "_")
        side, finger_name = finger.split(" ", 1)
        filename = f"{side}_{finger_name.replace(' ', '_')}_{safe_pattern}.bmp"
        filepath = os.path.join("data", self.patient_uuid, filename)
        cv2.imwrite(filepath, self.current_captured_image)

        # Update captured fingers
        self.captured_fingers[finger] = {"pattern": self.current_pattern, "file": filename}
        self._update_captured_summary()
        self.ui.progressLabel.setText(f"Progress: {len(self.captured_fingers)}/10 fingers captured")
        self.ui.nextFingerButton.setEnabled(True)
        self.ui.retakeCurrentButton.setEnabled(True)
        self.ui.saveCurrentFingerButton.setEnabled(False)
        self._reset_capture_ui()

    def _on_next_finger(self):
        """Advance to the next uncaptured finger."""
        for i in range(self.current_finger_index + 1, len(self.finger_order)):
            finger = self.finger_order[i]
            if finger not in self.captured_fingers:
                self.current_finger_index = i
                self._update_finger_selection()
                self._reset_capture_ui()
                return
        QMessageBox.information(self, "Info", "All fingers have been captured.")

    def _on_retake_current(self):
        """Retake the current finger's capture."""
        finger = self.ui.fingerSelectionComboBox.currentText()
        if finger in self.captured_fingers:
            filepath = os.path.join("data", self.patient_uuid, self.captured_fingers[finger]['file'])
            if os.path.exists(filepath):
                os.remove(filepath)
            del self.captured_fingers[finger]
            self._update_captured_summary()
            self.ui.progressLabel.setText(f"Progress: {len(self.captured_fingers)}/10 fingers captured")
            self._reset_capture_ui()
        else:
            QMessageBox.warning(self, "Warning", "No capture to retake for this finger.")

    def _reset_capture_ui(self):
        """Reset the capture UI to idle state."""
        self.ui.predictionResultBrowser.setVisible(False)
        self.ui.agreeButton.setVisible(False)
        self.ui.disagreeButton.setVisible(False)
        self.ui.manualPatternWidget.setVisible(False)
        self.ui.saveCurrentFingerButton.setEnabled(False)
        self.ui.retakeCurrentButton.setEnabled(False)
        self.ui.captureButton.setText("🎥 Start Preview")
        self.is_preview_active = False
        self.current_captured_image = None
        self.current_pattern = None
        self.ui.fingerprintImageLabel.setPixmap(QPixmap("icon.svg"))

    def _update_finger_selection(self):
        """Update the finger selection combo box and progress label."""
        if self.current_finger_index < len(self.finger_order):
            finger = self.finger_order[self.current_finger_index]
            index = self.ui.fingerSelectionComboBox.findText(finger)
            if index >= 0:
                self.ui.fingerSelectionComboBox.setCurrentIndex(index)
            self.ui.progressLabel.setText(f"Progress: {len(self.captured_fingers)}/10 fingers captured")
        else:
            self.ui.fingerSelectionComboBox.setCurrentIndex(0)
            self.ui.progressLabel.setText("All 10 fingers captured")

    def _update_captured_summary(self):
        """Update the captured fingerprints summary text."""
        if not self.captured_fingers:
            self.ui.capturedFingersListLabel.setText("No fingerprints captured yet.")
        else:
            text = "Captured fingerprints:\n"
            for finger, data in self.captured_fingers.items():
                text += f"{finger}: {data['pattern']}\n"
            self.ui.capturedFingersListLabel.setText(text)

    def _on_save_all_data(self):
        """Save all patient data to a JSON file."""
        if not self._validate_form():
            QMessageBox.warning(self, "Form Incomplete", "Please complete all required patient information.")
            return
        if len(self.captured_fingers) < 10:
            QMessageBox.warning(self, "Fingerprints Incomplete", "Please capture all 10 fingerprints.")
            return

        data = {
            "uuid": self.patient_uuid,
            "full_name": self.ui.nameLineEdit.text().strip(),
            "age": int(self.ui.ageLineEdit.text().strip()),
            "gender": self.ui.genderComboBox.currentText(),
            "group": self.ui.groupComboBox.currentText(),
            "smoking_status": self.ui.smokingComboBox.currentText(),
            "medical_conditions": [],
            "periodontal_disease": self.ui.dentalDiseaseCheckBox.isChecked(),
            "dental_condition": self.ui.dentalDiseaseTypeLineEdit.text().strip() if self.ui.dentalDiseaseCheckBox.isChecked() else "",
            "measurements": {
                "pd_mm": float(self.ui.pdLineEdit.text().strip()) if self.ui.pdLineEdit.text().strip() else None,
                "cal_mm": float(self.ui.calLineEdit.text().strip()) if self.ui.calLineEdit.text().strip() else None,
                "hba1c_pct": float(self.ui.hba1cLineEdit.text().strip()) if self.ui.hba1cLineEdit.text().strip() else None
            },
            "fingerprints": [
                {"finger": finger, "pattern": info["pattern"], "file": info["file"]}
                for finger, info in self.captured_fingers.items()
            ],
            "schema_version": 1
        }

        # Add medical conditions
        for checkbox, condition in [
            (self.ui.diabetesCheckBox, "Type 2 Diabetes"),
            (self.ui.hypertensionCheckBox, "Hypertension"),
            (self.ui.heartDiseaseCheckBox, "Cardiovascular Disease"),
            (self.ui.asthmaCheckBox, "Asthma/COPD")
        ]:
            if checkbox.isChecked():
                data["medical_conditions"].append(condition)

        # Save to JSON
        try:
            filepath = os.path.join("data", self.patient_uuid, "patient.json")
            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
            QMessageBox.information(self, "Success", "Patient data saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save patient data: {str(e)}")

    def _on_clear_all_data(self):
        """Clear all entered data and captured fingerprints."""
        if (self.patient_uuid or len(self.captured_fingers) > 0 or
            any(field.text().strip() for field in [self.ui.nameLineEdit, self.ui.ageLineEdit])):
            reply = QMessageBox.question(
                self, "Confirm Clear", "Do you really want to delete all current patient data?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                # Delete patient folder if exists
                if self.patient_uuid and os.path.exists(os.path.join("data", self.patient_uuid)):
                    import shutil
                    shutil.rmtree(os.path.join("data", self.patient_uuid))

                # Reset form fields
                for widget in [self.ui.nameLineEdit, self.ui.ageLineEdit, self.ui.pdLineEdit,
                              self.ui.calLineEdit, self.ui.hba1cLineEdit, self.ui.dentalDiseaseTypeLineEdit,
                              self.ui.medicationsTextEdit]:
                    widget.clear()
                for combobox in [self.ui.genderComboBox, self.ui.groupComboBox, self.ui.smokingComboBox]:
                    combobox.setCurrentIndex(0)
                for checkbox in [self.ui.diabetesCheckBox, self.ui.hypertensionCheckBox,
                                self.ui.heartDiseaseCheckBox, self.ui.asthmaCheckBox,
                                self.ui.dentalDiseaseCheckBox]:
                    checkbox.setChecked(False)
                self.ui.dentalDiseaseTypeLineEdit.setEnabled(False)

                # Reset fingerprint data
                self.captured_fingers.clear()
                self._update_captured_summary()
                self.ui.progressLabel.setText("Progress: 0/10 fingers captured")
                self.patient_uuid = None
                self.current_finger_index = 0
                self._update_finger_selection()
                self._reset_capture_ui()
                self.capture_controller.stop_preview()

    def closeEvent(self, event):
        """Handle window close event to clean up resources."""
        self.capture_controller.cleanup()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())