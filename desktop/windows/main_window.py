import sys
import os
import uuid
import json
import cv2
from PySide6.QtCore import Qt, QTimer, QThread, Signal, Slot
from PySide6.QtGui import QPixmap, QImage, QIntValidator, QRegularExpressionValidator, QDoubleValidator
from PySide6.QtWidgets import QMainWindow, QMessageBox, QApplication
from UI.ui import Ui_MainWindow
from core.fingerprint_controller import FingerprintCaptureController
from PySide6.QtCore import QRegularExpression


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
        self.ui.dentalDiseaseCheckBox.toggled.connect(self.ui.dentalDiseaseTypeLineEdit.setEnabled)
        self.ui.dentalDiseaseCheckBox.stateChanged.connect(self._update_button_states)
        self.ui.dentalDiseaseTypeLineEdit.textChanged.connect(self._update_button_states)

        name_regex = QRegularExpression("[a-zA-Z\\s]*")
        name_validator = QRegularExpressionValidator(name_regex, self.ui.nameLineEdit)
        self.ui.nameLineEdit.setValidator(name_validator)
        age_validator = QIntValidator(1, 120, self.ui.ageLineEdit)
        self.ui.ageLineEdit.setValidator(age_validator)
        pd_cal_validator = QDoubleValidator(0.0, 15.0, 2, self.ui.pdLineEdit)
        pd_cal_validator.setNotation(QDoubleValidator.StandardNotation)
        self.ui.pdLineEdit.setValidator(pd_cal_validator)
        self.ui.calLineEdit.setValidator(pd_cal_validator)
        hba1c_validator = QDoubleValidator(0.0, 20.0, 2, self.ui.hba1cLineEdit)
        hba1c_validator.setNotation(QDoubleValidator.StandardNotation)
        self.ui.hba1cLineEdit.setValidator(hba1c_validator)

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

    # def _on_dental_disease_checked(self, state):
    #     """Enable/disable dental condition field based on checkbox."""
    #     self.ui.dentalDiseaseTypeLineEdit.setEnabled(state == Qt.Checked)

    def _validate_form_for_preview(self):
        """Validate form for preview - only requires name."""
        name = self.ui.nameLineEdit.text().strip()
        return bool(name)

    def _validate_form_for_complete_save(self):
        """Validate all required patient information fields for complete save."""
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

    def _validate_form_for_partial_save(self):
        """Validate form for partial save - only requires name and at least one fingerprint."""
        name = self.ui.nameLineEdit.text().strip()
        has_fingerprints = len(self.captured_fingers) > 0
        return bool(name) and has_fingerprints

    def _toggle_preview(self):
        """Toggle between preview and capture modes with better error handling"""
        try:
            if not self.is_preview_active:
                if not self._validate_form_for_preview():
                    QMessageBox.warning(self, "Form Incomplete", 
                                      "Please enter at least a patient name before starting preview.")
                    return
                
                # Start preview in thread
                if self.capture_controller.start_preview():
                    self.is_preview_active = True
                    self.ui.captureButton.setText("📷 Capture Image")
                    self.ui.captureButton.setEnabled(True)
                    
                    # Hide prediction UI during preview
                    self.ui.predictionResultBrowser.setVisible(False)
                    self.ui.agreeButton.setVisible(False)
                    self.ui.disagreeButton.setVisible(False)
                    self.ui.manualPatternWidget.setVisible(False)
                else:
                    QMessageBox.warning(self, "Error", "Failed to start fingerprint preview")
            else:
                # Capture current frame
                self.capture_controller.stop_preview()
                self.is_preview_active = False
                self.ui.captureButton.setText("🎥 Start Preview")
                
                # Get the current captured image
                self.current_captured_image = self.capture_controller.current_image
                
                if self.current_captured_image is not None:
                    # Simulate AI prediction (you can replace this with actual AI model)
                    predicted_pattern = self._get_ai_prediction(self.current_captured_image)
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
                    QMessageBox.warning(self, "Error", "Failed to capture image. Please try again.")
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            self.is_preview_active = False
            self.ui.captureButton.setText("🎥 Start Preview")

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
        
        # Only set default image if no fingerprint device is active
        if not self.capture_controller.is_preview_active:
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
        """Save all patient data to a JSON file with flexible validation."""
        # Check if we can save with partial data
        if self._validate_form_for_complete_save() and len(self.captured_fingers) == 10:
            # Complete save with all data
            self._save_patient_data(complete=True)
        elif self._validate_form_for_partial_save():
            # Partial save with name and some fingerprints
            reply = QMessageBox.question(
                self, "Partial Save", 
                f"You have captured {len(self.captured_fingers)} fingerprint(s) but some patient information is missing.\n\n"
                "Do you want to save the available data?",
                QMessageBox.Yes | QMessageBox.No, 
                QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                self._save_patient_data(complete=False)
        else:
            if not self.ui.nameLineEdit.text().strip():
                QMessageBox.warning(self, "Missing Information", "Please enter at least a patient name.")
            elif len(self.captured_fingers) == 0:
                QMessageBox.warning(self, "No Fingerprints", "Please capture at least one fingerprint.")

    def _save_patient_data(self, complete=True):
        """Save patient data with flexible field handling."""
        try:
            # Generate UUID and folder if not exists
            if self.patient_uuid is None:
                self.patient_uuid = str(uuid.uuid4())
                os.makedirs(os.path.join("data", self.patient_uuid), exist_ok=True)

            # Build data with available information
            data = {
                "uuid": self.patient_uuid,
                "full_name": self.ui.nameLineEdit.text().strip(),
                "fingerprints": [
                    {"finger": finger, "pattern": info["pattern"], "file": info["file"]}
                    for finger, info in self.captured_fingers.items()
                ],
                "schema_version": 1,
                "save_type": "complete" if complete else "partial"
            }

            # Add optional fields if they have values
            age_text = self.ui.ageLineEdit.text().strip()
            if age_text:
                try:
                    data["age"] = int(age_text)
                except ValueError:
                    data["age"] = None
            else:
                data["age"] = None

            # Add other optional fields
            data["gender"] = self.ui.genderComboBox.currentText() if self.ui.genderComboBox.currentIndex() > 0 else ""
            data["group"] = self.ui.groupComboBox.currentText() if self.ui.groupComboBox.currentIndex() > 0 else ""
            data["smoking_status"] = self.ui.smokingComboBox.currentText() if self.ui.smokingComboBox.currentIndex() > 0 else ""

            # Medical conditions
            data["medical_conditions"] = []
            for checkbox, condition in [
                (self.ui.diabetesCheckBox, "Type 2 Diabetes"),
                (self.ui.hypertensionCheckBox, "Hypertension"),
                (self.ui.heartDiseaseCheckBox, "Cardiovascular Disease"),
                (self.ui.asthmaCheckBox, "Asthma/COPD")
            ]:
                if checkbox.isChecked():
                    data["medical_conditions"].append(condition)

            # Dental information
            data["periodontal_disease"] = self.ui.dentalDiseaseCheckBox.isChecked()
            data["dental_condition"] = self.ui.dentalDiseaseTypeLineEdit.text().strip() if self.ui.dentalDiseaseCheckBox.isChecked() else ""

            # Measurements
            data["measurements"] = {
                "pd_mm": float(self.ui.pdLineEdit.text().strip()) if self.ui.pdLineEdit.text().strip() else None,
                "cal_mm": float(self.ui.calLineEdit.text().strip()) if self.ui.calLineEdit.text().strip() else None,
                "hba1c_pct": float(self.ui.hba1cLineEdit.text().strip()) if self.ui.hba1cLineEdit.text().strip() else None
            }

            # Save to JSON
            filepath = os.path.join("data", self.patient_uuid, "patient.json")
            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
            
            save_type = "Complete" if complete else "Partial"
            QMessageBox.information(self, "Success", f"{save_type} patient data saved successfully!\nFingerprints captured: {len(self.captured_fingers)}")

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
                if hasattr(self, 'capture_controller'):
                    self.capture_controller.stop_preview()

    def _get_ai_prediction(self, image):
        """Placeholder for AI prediction - replace with actual AI model"""
        # This is where you would integrate your actual fingerprint pattern recognition AI model
        # For now, returning a default pattern
        return "Plain Arch"

    def _update_button_states(self):
        """Update button states based on form validity and fingerprint progress with thread safety"""
        try:
            has_name = bool(self.ui.nameLineEdit.text().strip())
            has_fingerprints = len(self.captured_fingers) > 0
            is_complete_form = self._validate_form_for_complete_save()
            all_fingers_captured = len(self.captured_fingers) == 10
            
            # Enable capture button if name is entered
            self.ui.captureButton.setEnabled(has_name)
            
            # Enable save button if we have name and fingerprints OR complete form
            can_save = (has_name and has_fingerprints) or (is_complete_form and all_fingers_captured)
            self.ui.saveAllDataButton.setEnabled(can_save)
            
        except Exception as e:
            print(f"Error updating button states: {e}")

    def _handle_capture_error(self, error_message):
        """Handle capture errors gracefully"""
        QMessageBox.warning(self, "Capture Error", f"Error during fingerprint capture: {error_message}")
        self.is_preview_active = False
        self.ui.captureButton.setText("🎥 Start Preview")
        self.ui.captureButton.setEnabled(True)

    def closeEvent(self, event):
        """Handle window close event to clean up resources properly"""
        try:
            # Stop any ongoing operations
            if hasattr(self, 'capture_controller'):
                self.capture_controller.cleanup()
            event.accept()
        except Exception as e:
            print(f"Error during cleanup: {e}")
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
