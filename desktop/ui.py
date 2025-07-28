# -*- coding: utf-8 -*-

################################################################################
## Organized Fingerprint Recognition UI
## Improved structure with better maintainability and proper dropdown values
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QTextBrowser,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    """
    Main UI class for Fingerprint Recognition System
    Organized into logical sections for better maintainability
    """
    
    def setupUi(self, MainWindow):
        """Main setup method - calls all sub-methods in logical order"""
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        
        # Window configuration
        MainWindow.resize(747, 800)
        MainWindow.setStyleSheet(u"background-color: rgb(15, 23, 42);")
        
        # Setup main structure
        self._setup_main_container(MainWindow)
        
        # Setup all sections
        self._setup_header_section()
        self._setup_patient_info_section()
        self._setup_fingerprint_section()
        self._setup_scanner_section()
        self._setup_prediction_section()
        self._setup_captured_fingers_section()
        self._setup_final_actions_section()
        
        # Finalize setup
        self._finalize_setup(MainWindow)

    def _setup_main_container(self, MainWindow):
        """Setup the main container and scroll area"""
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        
        # Main scroll area
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"border:0px;")
        self.scrollArea.setWidgetResizable(True)
        
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 712, 1535))
        
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")

    def _setup_header_section(self):
        """Setup the header with title and navigation buttons"""
        self.headerWidget = QWidget(self.scrollAreaWidgetContents)
        self.headerWidget.setObjectName(u"headerWidget")
        self.headerWidget.setMinimumSize(QSize(480, 84))
        self.headerWidget.setMaximumSize(QSize(16777215, 84))
        self.headerWidget.setStyleSheet(u"QWidget{background-color: #0f172a;padding: 10px 20px;}")
        
        self.horizontalLayout = QHBoxLayout(self.headerWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        
        # Title and buttons container
        self.widget = QWidget(self.headerWidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        
        # Title label
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(256, 0))
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);font-size: 18px;font-weight: bold;")
        self.horizontalLayout_2.addWidget(self.label)
        
        # Navigation buttons
        self._setup_header_buttons()
        
        self.horizontalLayout_2.addWidget(self.widget_2)
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout_4.addWidget(self.headerWidget)

    def _setup_header_buttons(self):
        """Setup header navigation buttons"""
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        
        button_style = u"QPushButton{color: #d1d5db;font-size: 14px;background: transparent;border: none;padding: 4px 12px;}QPushButton:hover{color: #ffffff;}"
        
        self.pushButton = QPushButton(self.widget_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(button_style)
        self.pushButton.setFlat(True)
        self.horizontalLayout_3.addWidget(self.pushButton)
        
        self.pushButton_2 = QPushButton(self.widget_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(button_style)
        self.pushButton_2.setFlat(True)
        self.horizontalLayout_3.addWidget(self.pushButton_2)

    def _setup_patient_info_section(self):
        """Setup patient information form section"""
        # Section header
        self.textBrowser = QTextBrowser(self.scrollAreaWidgetContents)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setMaximumSize(QSize(16777215, 70))
        font = QFont()
        font.setFamilies([u"Segoe UI Semibold"])
        font.setBold(True)
        self.textBrowser.setFont(font)
        self.textBrowser.setLayoutDirection(Qt.LeftToRight)
        self.textBrowser.setStyleSheet(u"border:0px;")
        self.verticalLayout_4.addWidget(self.textBrowser)
        
        # Patient info form
        self._setup_patient_form()

    def _setup_patient_form(self):
        """Setup the patient information form with all fields"""
        self.patientInfoWidget = QWidget(self.scrollAreaWidgetContents)
        self.patientInfoWidget.setObjectName(u"patientInfoWidget")
        self.patientInfoWidget.setStyleSheet(self._get_form_styles())
        
        self.patientInfoGridLayout = QGridLayout(self.patientInfoWidget)
        self.patientInfoGridLayout.setObjectName(u"patientInfoGridLayout")
        
        # Setup form fields
        self._setup_basic_info_fields()
        self._setup_medical_info_fields()
        self._setup_clinical_measurements()
        self._setup_dental_info_fields()
        
        self.verticalLayout_4.addWidget(self.patientInfoWidget)

    def _setup_basic_info_fields(self):
        """Setup basic patient information fields (Name, Age, Gender, Group)"""
        # Name field
        self.nameLabel = QLabel(self.patientInfoWidget)
        self.nameLabel.setObjectName(u"nameLabel")
        self.patientInfoGridLayout.addWidget(self.nameLabel, 0, 0, 1, 1)
        
        self.nameLineEdit = QLineEdit(self.patientInfoWidget)
        self.nameLineEdit.setObjectName(u"nameLineEdit")
        self.patientInfoGridLayout.addWidget(self.nameLineEdit, 0, 1, 1, 1)
        
        # Age field
        self.ageLabel = QLabel(self.patientInfoWidget)
        self.ageLabel.setObjectName(u"ageLabel")
        self.patientInfoGridLayout.addWidget(self.ageLabel, 0, 2, 1, 1)
        
        self.ageLineEdit = QLineEdit(self.patientInfoWidget)
        self.ageLineEdit.setObjectName(u"ageLineEdit")
        self.patientInfoGridLayout.addWidget(self.ageLineEdit, 0, 3, 1, 1)
        
        # Gender field
        self.genderLabel = QLabel(self.patientInfoWidget)
        self.genderLabel.setObjectName(u"genderLabel")
        self.patientInfoGridLayout.addWidget(self.genderLabel, 1, 0, 1, 1)
        
        self.genderComboBox = QComboBox(self.patientInfoWidget)
        self._populate_gender_dropdown()
        self.genderComboBox.setObjectName(u"genderComboBox")
        self.genderComboBox.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.patientInfoGridLayout.addWidget(self.genderComboBox, 1, 1, 1, 1)
        
        # Group field
        self.groupLabel = QLabel(self.patientInfoWidget)
        self.groupLabel.setObjectName(u"groupLabel")
        self.patientInfoGridLayout.addWidget(self.groupLabel, 1, 2, 1, 1)
        
        self.groupComboBox = QComboBox(self.patientInfoWidget)
        self._populate_group_dropdown()
        self.groupComboBox.setObjectName(u"groupComboBox")
        self.groupComboBox.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.patientInfoGridLayout.addWidget(self.groupComboBox, 1, 3, 1, 1)

    def _setup_medical_info_fields(self):
        """Setup medical information fields (Smoking, Diagnosis Source, Conditions)"""
        # Smoking field
        self.smokingLabel = QLabel(self.patientInfoWidget)
        self.smokingLabel.setObjectName(u"smokingLabel")
        self.patientInfoGridLayout.addWidget(self.smokingLabel, 2, 0, 1, 1)
        
        self.smokingComboBox = QComboBox(self.patientInfoWidget)
        self._populate_smoking_dropdown()
        self.smokingComboBox.setObjectName(u"smokingComboBox")
        self.smokingComboBox.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.patientInfoGridLayout.addWidget(self.smokingComboBox, 2, 1, 1, 1)
        
        # Diagnosis Source field
        self.diagnosisSourceLabel = QLabel(self.patientInfoWidget)
        self.diagnosisSourceLabel.setObjectName(u"diagnosisSourceLabel")
        self.patientInfoGridLayout.addWidget(self.diagnosisSourceLabel, 2, 2, 1, 1)
        
        self.diagnosisSourceComboBox = QComboBox(self.patientInfoWidget)
        self._populate_diagnosis_source_dropdown()
        self.diagnosisSourceComboBox.setObjectName(u"diagnosisSourceComboBox")
        self.diagnosisSourceComboBox.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.patientInfoGridLayout.addWidget(self.diagnosisSourceComboBox, 2, 3, 1, 1)
        
        # Medical conditions checkboxes
        self._setup_medical_conditions()
        
        # Medications field
        self.medicationsLabel = QLabel(self.patientInfoWidget)
        self.medicationsLabel.setObjectName(u"medicationsLabel")
        self.patientInfoGridLayout.addWidget(self.medicationsLabel, 4, 0, 1, 1)
        
        self.medicationsTextEdit = QTextEdit(self.patientInfoWidget)
        self.medicationsTextEdit.setObjectName(u"medicationsTextEdit")
        self.medicationsTextEdit.setMaximumSize(QSize(16777215, 60))
        self.patientInfoGridLayout.addWidget(self.medicationsTextEdit, 4, 1, 1, 3)

    def _setup_medical_conditions(self):
        """Setup medical conditions checkboxes"""
        self.medicalConditionsLabel = QLabel(self.patientInfoWidget)
        self.medicalConditionsLabel.setObjectName(u"medicalConditionsLabel")
        self.patientInfoGridLayout.addWidget(self.medicalConditionsLabel, 3, 0, 1, 1)
        
        self.medicalConditionsWidget = QWidget(self.patientInfoWidget)
        self.medicalConditionsWidget.setObjectName(u"medicalConditionsWidget")
        self.medicalConditionsLayout = QHBoxLayout(self.medicalConditionsWidget)
        self.medicalConditionsLayout.setObjectName(u"medicalConditionsLayout")
        
        # Individual checkboxes
        self.diabetesCheckBox = QCheckBox(self.medicalConditionsWidget)
        self.diabetesCheckBox.setObjectName(u"diabetesCheckBox")
        self.medicalConditionsLayout.addWidget(self.diabetesCheckBox)
        
        self.hypertensionCheckBox = QCheckBox(self.medicalConditionsWidget)
        self.hypertensionCheckBox.setObjectName(u"hypertensionCheckBox")
        self.medicalConditionsLayout.addWidget(self.hypertensionCheckBox)
        
        self.heartDiseaseCheckBox = QCheckBox(self.medicalConditionsWidget)
        self.heartDiseaseCheckBox.setObjectName(u"heartDiseaseCheckBox")
        self.medicalConditionsLayout.addWidget(self.heartDiseaseCheckBox)
        
        self.asthmaCheckBox = QCheckBox(self.medicalConditionsWidget)
        self.asthmaCheckBox.setObjectName(u"asthmaCheckBox")
        self.medicalConditionsLayout.addWidget(self.asthmaCheckBox)
        
        self.patientInfoGridLayout.addWidget(self.medicalConditionsWidget, 3, 1, 1, 3)

    def _setup_clinical_measurements(self):
        """Setup clinical measurement fields (PD, CAL, HbA1c)"""
        # PD field
        self.pdLabel = QLabel(self.patientInfoWidget)
        self.pdLabel.setObjectName(u"pdLabel")
        self.patientInfoGridLayout.addWidget(self.pdLabel, 5, 0, 1, 1)
        
        self.pdLineEdit = QLineEdit(self.patientInfoWidget)
        self.pdLineEdit.setObjectName(u"pdLineEdit")
        self.patientInfoGridLayout.addWidget(self.pdLineEdit, 5, 1, 1, 1)
        
        # CAL field
        self.calLabel = QLabel(self.patientInfoWidget)
        self.calLabel.setObjectName(u"calLabel")
        self.patientInfoGridLayout.addWidget(self.calLabel, 5, 2, 1, 1)
        
        self.calLineEdit = QLineEdit(self.patientInfoWidget)
        self.calLineEdit.setObjectName(u"calLineEdit")
        self.patientInfoGridLayout.addWidget(self.calLineEdit, 5, 3, 1, 1)
        
        # HbA1c field
        self.hba1cLabel = QLabel(self.patientInfoWidget)
        self.hba1cLabel.setObjectName(u"hba1cLabel")
        self.patientInfoGridLayout.addWidget(self.hba1cLabel, 6, 0, 1, 1)
        
        self.hba1cLineEdit = QLineEdit(self.patientInfoWidget)
        self.hba1cLineEdit.setObjectName(u"hba1cLineEdit")
        self.patientInfoGridLayout.addWidget(self.hba1cLineEdit, 6, 1, 1, 1)

    def _setup_dental_info_fields(self):
        """Setup dental information fields"""
        # Dental disease checkbox
        self.dentalDiseaseLabel = QLabel(self.patientInfoWidget)
        self.dentalDiseaseLabel.setObjectName(u"dentalDiseaseLabel")
        self.patientInfoGridLayout.addWidget(self.dentalDiseaseLabel, 6, 2, 1, 1)
        
        self.dentalDiseaseCheckBox = QCheckBox(self.patientInfoWidget)
        self.dentalDiseaseCheckBox.setObjectName(u"dentalDiseaseCheckBox")
        self.patientInfoGridLayout.addWidget(self.dentalDiseaseCheckBox, 6, 3, 1, 1)
        
        # Dental disease type field
        self.dentalDiseaseTypeLabel = QLabel(self.patientInfoWidget)
        self.dentalDiseaseTypeLabel.setObjectName(u"dentalDiseaseTypeLabel")
        self.patientInfoGridLayout.addWidget(self.dentalDiseaseTypeLabel, 7, 0, 1, 1)
        
        self.dentalDiseaseTypeLineEdit = QLineEdit(self.patientInfoWidget)
        self.dentalDiseaseTypeLineEdit.setObjectName(u"dentalDiseaseTypeLineEdit")
        self.dentalDiseaseTypeLineEdit.setEnabled(False)
        self.patientInfoGridLayout.addWidget(self.dentalDiseaseTypeLineEdit, 7, 1, 1, 3)

    def _setup_fingerprint_section(self):
        """Setup fingerprint collection section"""
        # Section header
        self.fingerprintSectionHeader = QTextBrowser(self.scrollAreaWidgetContents)
        self.fingerprintSectionHeader.setObjectName(u"fingerprintSectionHeader")
        self.fingerprintSectionHeader.setMaximumSize(QSize(16777215, 70))
        font = QFont()
        font.setFamilies([u"Segoe UI Semibold"])
        font.setBold(True)
        self.fingerprintSectionHeader.setFont(font)
        self.fingerprintSectionHeader.setStyleSheet(u"border:0px;")
        self.verticalLayout_4.addWidget(self.fingerprintSectionHeader)
        
        # Finger selection
        self._setup_finger_selection()

    def _setup_finger_selection(self):
        """Setup finger selection dropdown and progress"""
        self.fingerSelectionWidget = QWidget(self.scrollAreaWidgetContents)
        self.fingerSelectionWidget.setObjectName(u"fingerSelectionWidget")
        self.fingerSelectionWidget.setStyleSheet(self._get_dropdown_styles())
        
        self.fingerSelectionLayout = QHBoxLayout(self.fingerSelectionWidget)
        self.fingerSelectionLayout.setObjectName(u"fingerSelectionLayout")
        
        # Current finger label
        self.currentFingerLabel = QLabel(self.fingerSelectionWidget)
        self.currentFingerLabel.setObjectName(u"currentFingerLabel")
        self.fingerSelectionLayout.addWidget(self.currentFingerLabel)
        
        # Finger selection dropdown
        self.fingerSelectionComboBox = QComboBox(self.fingerSelectionWidget)
        self._populate_finger_selection_dropdown()
        self.fingerSelectionComboBox.setObjectName(u"fingerSelectionComboBox")
        self.fingerSelectionComboBox.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.fingerSelectionLayout.addWidget(self.fingerSelectionComboBox)
        
        # Progress label
        self.progressLabel = QLabel(self.fingerSelectionWidget)
        self.progressLabel.setObjectName(u"progressLabel")
        self.fingerSelectionLayout.addWidget(self.progressLabel)
        
        self.verticalLayout_4.addWidget(self.fingerSelectionWidget, 0, Qt.AlignHCenter)

    def _setup_scanner_section(self):
        """Setup fingerprint scanner section"""
        self.scannerContainer = QWidget(self.scrollAreaWidgetContents)
        self.scannerContainer.setObjectName(u"scannerContainer")
        self.verticalLayout_2 = QVBoxLayout(self.scannerContainer)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        
        # Scanner frame
        self._setup_scanner_frame()
        
        # Capture button
        self.captureButton = QPushButton(self.scannerContainer)
        self.captureButton.setObjectName(u"captureButton")
        self.captureButton.setStyleSheet(self._get_button_style("neutral"))
        self.verticalLayout_2.addWidget(self.captureButton, 0, Qt.AlignHCenter)
        
        # Prediction result display
        self.predictionResultBrowser = QTextBrowser(self.scannerContainer)
        self.predictionResultBrowser.setObjectName(u"predictionResultBrowser")
        self.predictionResultBrowser.setMaximumSize(QSize(16777215, 80))
        self.predictionResultBrowser.setStyleSheet(u"border:0px;")
        self.verticalLayout_2.addWidget(self.predictionResultBrowser)
        
        self.verticalLayout_4.addWidget(self.scannerContainer)

    def _setup_scanner_frame(self):
        """Setup the scanner frame with fingerprint image display"""
        self.scannerFrame = QWidget(self.scannerContainer)
        self.scannerFrame.setObjectName(u"scannerFrame")
        self.scannerFrame.setMinimumSize(QSize(300, 300))
        self.scannerFrame.setStyleSheet(u"background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e293b, stop:1 #0f172a);border-radius: 16px;border: 1px solid #475569;padding: 32px;")
        
        self.verticalLayout_3 = QVBoxLayout(self.scannerFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        
        self.fingerprintImageLabel = QLabel(self.scannerFrame)
        self.fingerprintImageLabel.setObjectName(u"fingerprintImageLabel")
        self.fingerprintImageLabel.setMinimumSize(QSize(251, 281))
        self.fingerprintImageLabel.setStyleSheet(u"border:0px;background-color: transparent;")
        self.fingerprintImageLabel.setPixmap(QPixmap(u"icon.svg"))
        self.fingerprintImageLabel.setScaledContents(True)
        self.fingerprintImageLabel.setAlignment(Qt.AlignCenter)
        
        self.verticalLayout_3.addWidget(self.fingerprintImageLabel, 0, Qt.AlignHCenter|Qt.AlignVCenter)
        self.verticalLayout_2.addWidget(self.scannerFrame)

    def _setup_prediction_section(self):
        """Setup prediction response section"""
        # Prediction response buttons
        self.predictionResponseWidget = QWidget(self.scrollAreaWidgetContents)
        self.predictionResponseWidget.setObjectName(u"predictionResponseWidget")
        self.predictionResponseLayout = QHBoxLayout(self.predictionResponseWidget)
        self.predictionResponseLayout.setObjectName(u"predictionResponseLayout")
        
        # Agree button
        self.agreeButton = QPushButton(self.predictionResponseWidget)
        self.agreeButton.setObjectName(u"agreeButton")
        self.agreeButton.setStyleSheet(self._get_button_style("success"))
        self.predictionResponseLayout.addWidget(self.agreeButton)
        
        # Disagree button
        self.disagreeButton = QPushButton(self.predictionResponseWidget)
        self.disagreeButton.setObjectName(u"disagreeButton")
        self.disagreeButton.setStyleSheet(self._get_button_style("danger"))
        self.predictionResponseLayout.addWidget(self.disagreeButton)
        
        self.verticalLayout_4.addWidget(self.predictionResponseWidget)
        
        # Manual pattern selection
        self._setup_manual_pattern_selection()
        
        # Fingerprint actions
        self._setup_fingerprint_actions()

    def _setup_manual_pattern_selection(self):
        """Setup manual pattern selection for disagreement cases"""
        self.manualPatternWidget = QWidget(self.scrollAreaWidgetContents)
        self.manualPatternWidget.setObjectName(u"manualPatternWidget")
        self.manualPatternWidget.setStyleSheet(self._get_dropdown_styles())
        
        self.manualPatternLayout = QHBoxLayout(self.manualPatternWidget)
        self.manualPatternLayout.setObjectName(u"manualPatternLayout")
        
        self.manualPatternLabel = QLabel(self.manualPatternWidget)
        self.manualPatternLabel.setObjectName(u"manualPatternLabel")
        self.manualPatternLayout.addWidget(self.manualPatternLabel)
        
        self.fingerprintPatternComboBox = QComboBox(self.manualPatternWidget)
        self._populate_fingerprint_pattern_dropdown()
        self.fingerprintPatternComboBox.setObjectName(u"fingerprintPatternComboBox")
        self.fingerprintPatternComboBox.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.manualPatternLayout.addWidget(self.fingerprintPatternComboBox)
        
        self.verticalLayout_4.addWidget(self.manualPatternWidget)

    def _setup_fingerprint_actions(self):
        """Setup fingerprint action buttons"""
        self.fingerprintActionsWidget = QWidget(self.scrollAreaWidgetContents)
        self.fingerprintActionsWidget.setObjectName(u"fingerprintActionsWidget")
        self.fingerprintActionsLayout = QHBoxLayout(self.fingerprintActionsWidget)
        self.fingerprintActionsLayout.setObjectName(u"fingerprintActionsLayout")
        
        # Save current finger button
        self.saveCurrentFingerButton = QPushButton(self.fingerprintActionsWidget)
        self.saveCurrentFingerButton.setObjectName(u"saveCurrentFingerButton")
        self.saveCurrentFingerButton.setStyleSheet(self._get_button_style("success"))
        self.fingerprintActionsLayout.addWidget(self.saveCurrentFingerButton)
        
        # Next finger button
        self.nextFingerButton = QPushButton(self.fingerprintActionsWidget)
        self.nextFingerButton.setObjectName(u"nextFingerButton")
        self.nextFingerButton.setStyleSheet(self._get_button_style("primary"))
        self.fingerprintActionsLayout.addWidget(self.nextFingerButton)
        
        # Retake current button
        self.retakeCurrentButton = QPushButton(self.fingerprintActionsWidget)
        self.retakeCurrentButton.setObjectName(u"retakeCurrentButton")
        self.retakeCurrentButton.setStyleSheet(self._get_button_style("warning"))
        self.fingerprintActionsLayout.addWidget(self.retakeCurrentButton)
        
        self.verticalLayout_4.addWidget(self.fingerprintActionsWidget)

    def _setup_captured_fingers_section(self):
        """Setup captured fingerprints summary section"""
        # Section header
        self.capturedFingersHeader = QTextBrowser(self.scrollAreaWidgetContents)
        self.capturedFingersHeader.setObjectName(u"capturedFingersHeader")
        self.capturedFingersHeader.setMaximumSize(QSize(16777215, 50))
        self.capturedFingersHeader.setStyleSheet(u"border:0px;")
        self.verticalLayout_4.addWidget(self.capturedFingersHeader)
        
        # Captured fingers display area
        self.capturedFingersScrollArea = QScrollArea(self.scrollAreaWidgetContents)
        self.capturedFingersScrollArea.setObjectName(u"capturedFingersScrollArea")
        self.capturedFingersScrollArea.setMaximumSize(QSize(16777215, 200))
        self.capturedFingersScrollArea.setStyleSheet(u"background-color: #1e293b;border: 1px solid #475569;border-radius: 8px;")
        self.capturedFingersScrollArea.setWidgetResizable(True)
        
        self.capturedFingersContent = QWidget()
        self.capturedFingersContent.setObjectName(u"capturedFingersContent")
        self.capturedFingersContent.setGeometry(QRect(0, 0, 692, 69))
        
        self.capturedFingersLayout = QVBoxLayout(self.capturedFingersContent)
        self.capturedFingersLayout.setObjectName(u"capturedFingersLayout")
        
        self.capturedFingersListLabel = QLabel(self.capturedFingersContent)
        self.capturedFingersListLabel.setObjectName(u"capturedFingersListLabel")
        self.capturedFingersListLabel.setStyleSheet(u"color: white;font-size: 12px;padding: 10px;")
        self.capturedFingersListLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.capturedFingersListLabel.setWordWrap(True)
        self.capturedFingersLayout.addWidget(self.capturedFingersListLabel)
        
        self.capturedFingersScrollArea.setWidget(self.capturedFingersContent)
        self.verticalLayout_4.addWidget(self.capturedFingersScrollArea)

    def _setup_final_actions_section(self):
        """Setup final action buttons section"""
        self.finalActionsWidget = QWidget(self.scrollAreaWidgetContents)
        self.finalActionsWidget.setObjectName(u"finalActionsWidget")
        self.finalActionsLayout = QHBoxLayout(self.finalActionsWidget)
        self.finalActionsLayout.setObjectName(u"finalActionsLayout")
        
        # Save all data button
        self.saveAllDataButton = QPushButton(self.finalActionsWidget)
        self.saveAllDataButton.setObjectName(u"saveAllDataButton")
        self.saveAllDataButton.setEnabled(False)
        self.saveAllDataButton.setStyleSheet(self._get_button_style("success", large=True))
        self.finalActionsLayout.addWidget(self.saveAllDataButton)
        
        # Clear all data button
        self.clearAllDataButton = QPushButton(self.finalActionsWidget)
        self.clearAllDataButton.setObjectName(u"clearAllDataButton")
        self.clearAllDataButton.setStyleSheet(self._get_button_style("danger", large=True))
        self.finalActionsLayout.addWidget(self.clearAllDataButton)
        
        self.verticalLayout_4.addWidget(self.finalActionsWidget)

    def _finalize_setup(self, MainWindow):
        """Finalize the UI setup"""
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    # ========== DROPDOWN POPULATION METHODS ==========
    
    def _populate_gender_dropdown(self):
        """Populate gender dropdown with appropriate options"""
        gender_options = [
            "Select Gender",
            "Male",
            "Female", 
            "Non-binary",
            "Prefer not to say",
            "Other"
        ]
        for option in gender_options:
            self.genderComboBox.addItem(option)

    def _populate_group_dropdown(self):
        """Populate group dropdown with study/control groups"""
        group_options = [
            "Select Group",
            "Control Group",
            "Study Group A", 
            "Study Group B",
            "Study Group C",
            "Diabetes Group",
            "Hypertension Group",
            "Healthy Control"
        ]
        for option in group_options:
            self.groupComboBox.addItem(option)

    def _populate_smoking_dropdown(self):
        """Populate smoking status dropdown"""
        smoking_options = [
            "Select Smoking Status",
            "Never Smoked",
            "Former Smoker (>1 year)",
            "Former Smoker (<1 year)", 
            "Current Smoker (Light: <10/day)",
            "Current Smoker (Moderate: 10-20/day)",
            "Current Smoker (Heavy: >20/day)",
            "Occasional Smoker"
        ]
        for option in smoking_options:
            self.smokingComboBox.addItem(option)

    def _populate_diagnosis_source_dropdown(self):
        """Populate diagnosis source dropdown"""
        diagnosis_options = [
            "Select Diagnosis Source",
            "Clinical Examination",
            "Laboratory Blood Test",
            "Laboratory Urine Test",
            "X-Ray Imaging",
            "CT Scan",
            "MRI Scan",
            "Ultrasound",
            "Biopsy Results",
            "Self-Reported Symptoms",
            "Family History",
            "Previous Medical Records"
        ]
        for option in diagnosis_options:
            self.diagnosisSourceComboBox.addItem(option)

    def _populate_finger_selection_dropdown(self):
        """Populate finger selection dropdown"""
        finger_options = [
            "Select finger to capture",
            "Right Thumb",
            "Right Index Finger",
            "Right Middle Finger", 
            "Right Ring Finger",
            "Right Little Finger",
            "Left Thumb",
            "Left Index Finger",
            "Left Middle Finger",
            "Left Ring Finger", 
            "Left Little Finger"
        ]
        for option in finger_options:
            self.fingerSelectionComboBox.addItem(option)

    def _populate_fingerprint_pattern_dropdown(self):
        """Populate fingerprint pattern dropdown"""
        pattern_options = [
            "Select Fingerprint Pattern",
            "Plain Arch",
            "Tented Arch", 
            "Ulnar Loop",
            "Radial Loop",
            "Plain Whorl",
            "Central Pocket Loop Whorl",
            "Double Loop Whorl",
            "Accidental Whorl",
            "Spiral Whorl",
            "Composite Whorl",
            "Unclear/Damaged Print"
        ]
        for option in pattern_options:
            self.fingerprintPatternComboBox.addItem(option)

    # ========== STYLE METHODS ==========
    
    def _get_form_styles(self):
        """Get consistent form styling"""
        return u"""
        QLabel {
            color: white;
            font-size: 14px;
            font-weight: 500;
        }
        QLineEdit, QComboBox, QTextEdit {
            background-color: #1e293b;
            color: white;
            border: 1px solid #475569;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 14px;
        }
        QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
            border-color: #14b8a6;
            outline: none;
        }
        QCheckBox {
            color: white;
            font-size: 14px;
            spacing: 8px;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 1px solid #475569;
            border-radius: 3px;
            background-color: #1e293b;
        }
        QCheckBox::indicator:checked {
            background-color: #14b8a6;
            border-color: #14b8a6;
        }
        """

    def _get_dropdown_styles(self):
        """Get consistent dropdown styling"""
        return u"""
        QLabel {
            color: white;
            font-size: 14px;
            font-weight: 500;
        }
        QComboBox {
            background-color: #1e293b;
            color: white;
            border: 1px solid #475569;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 14px;
        }
        QComboBox:focus {
            border-color: #14b8a6;
            outline: none;
        }
        """

    def _get_button_style(self, button_type, large=False):
        """Get consistent button styling based on type"""
        size_suffix = "font-size: 16px;" if large else "font-size: 14px;"
        padding = "padding: 16px 32px;" if large else "padding: 12px 24px;"
        
        styles = {
            "primary": f"QPushButton{{background-color: #2563eb;color: white;border: 1px solid #3b82f6;{padding}border-radius: 8px;font-weight: 500;{size_suffix}}}QPushButton:hover{{background-color: #3b82f6;}}",
            "success": f"QPushButton{{background-color: #059669;color: white;border: 1px solid #10b981;{padding}border-radius: 8px;font-weight: 500;{size_suffix}}}QPushButton:hover{{background-color: #10b981;}}QPushButton:disabled{{background-color: #374151;color: #9ca3af;border-color: #4b5563;}}",
            "danger": f"QPushButton{{background-color: #dc2626;color: white;border: 1px solid #ef4444;{padding}border-radius: 8px;font-weight: 500;{size_suffix}}}QPushButton:hover{{background-color: #ef4444;}}",
            "warning": f"QPushButton{{background-color: #d97706;color: white;border: 1px solid #f59e0b;{padding}border-radius: 8px;font-weight: 500;{size_suffix}}}QPushButton:hover{{background-color: #f59e0b;}}",
            "neutral": f"QPushButton{{background-color: #475569;color: white;border: 1px solid #64748b;{padding}border-radius: 8px;font-weight: 500;{size_suffix}}}QPushButton:hover{{background-color: #64748b;}}"
        }
        return styles.get(button_type, styles["neutral"])

    # ========== UI TEXT SETUP ==========
    
    def retranslateUi(self, MainWindow):
        """Set all UI text and labels"""
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Fingerprint Recognition System", None))
        
        # Header section
        self.label.setText(QCoreApplication.translate("MainWindow", u"Fingerprint Recognition System", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Collect Data", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Edit Data", None))
        
        # Patient info section header
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">
p, li { white-space: pre-wrap; }
hr { height: 1px; border-width: 0; }
li.unchecked::marker { content: "\\2610"; }
li.checked::marker { content: "\\2612"; }
</style></head><body style=" font-family:'Segoe UI Semibold'; font-size:9pt; font-weight:700; font-style:normal;">
<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Segoe UI'; font-size:18pt; color:#ffffff;">Patient Information (Enter Once)</span></p></body></html>""", None))
        
        # Basic info labels and placeholders
        self.nameLabel.setText(QCoreApplication.translate("MainWindow", u"Full Name", None))
        self.nameLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter patient's full name", None))
        self.ageLabel.setText(QCoreApplication.translate("MainWindow", u"Age (years)", None))
        self.ageLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter age in years", None))
        self.genderLabel.setText(QCoreApplication.translate("MainWindow", u"Gender", None))
        self.groupLabel.setText(QCoreApplication.translate("MainWindow", u"Study Group", None))
        
        # Medical info labels
        self.smokingLabel.setText(QCoreApplication.translate("MainWindow", u"Smoking Status", None))
        self.diagnosisSourceLabel.setText(QCoreApplication.translate("MainWindow", u"Diagnosis Source", None))
        self.medicalConditionsLabel.setText(QCoreApplication.translate("MainWindow", u"Medical Conditions", None))
        
        # Medical condition checkboxes
        self.diabetesCheckBox.setText(QCoreApplication.translate("MainWindow", u"Type 2 Diabetes", None))
        self.hypertensionCheckBox.setText(QCoreApplication.translate("MainWindow", u"Hypertension", None))
        self.heartDiseaseCheckBox.setText(QCoreApplication.translate("MainWindow", u"Cardiovascular Disease", None))
        self.asthmaCheckBox.setText(QCoreApplication.translate("MainWindow", u"Asthma/COPD", None))
        
        # Medications and clinical measurements
        self.medicationsLabel.setText(QCoreApplication.translate("MainWindow", u"Current Medications", None))
        self.medicationsTextEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"List all current medications, dosages, and frequency...", None))
        self.pdLabel.setText(QCoreApplication.translate("MainWindow", u"Probing Depth (mm)", None))
        self.pdLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter average PD value", None))
        self.calLabel.setText(QCoreApplication.translate("MainWindow", u"Clinical Attachment Level (mm)", None))
        self.calLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter average CAL value", None))
        self.hba1cLabel.setText(QCoreApplication.translate("MainWindow", u"HbA1c Level (%)", None))
        self.hba1cLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter HbA1c percentage", None))
        
        # Dental info
        self.dentalDiseaseLabel.setText(QCoreApplication.translate("MainWindow", u"Periodontal Disease", None))
        self.dentalDiseaseCheckBox.setText(QCoreApplication.translate("MainWindow", u"Has Periodontal Disease", None))
        self.dentalDiseaseTypeLabel.setText(QCoreApplication.translate("MainWindow", u"Specific Condition", None))
        self.dentalDiseaseTypeLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Specify: Gingivitis, Periodontitis (mild/moderate/severe), Dental Caries, etc.", None))
        
        # Fingerprint section
        self.fingerprintSectionHeader.setHtml(QCoreApplication.translate("MainWindow", u"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">
p, li { white-space: pre-wrap; }
hr { height: 1px; border-width: 0; }
li.unchecked::marker { content: "\\2610"; }
li.checked::marker { content: "\\2612"; }
</style></head><body style=" font-family:'Segoe UI Semibold'; font-size:9pt; font-weight:700; font-style:normal;">
<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Segoe UI'; font-size:18pt; color:#ffffff;">Fingerprint Collection - All 10 Fingers</span></p></body></html>""", None))
        
        # Finger selection
        self.currentFingerLabel.setText(QCoreApplication.translate("MainWindow", u"Current Finger:", None))
        self.progressLabel.setText(QCoreApplication.translate("MainWindow", u"Progress: 0/10 fingers captured", None))
        
        # Scanner and prediction
        self.fingerprintImageLabel.setText("")
        self.captureButton.setText(QCoreApplication.translate("MainWindow", u"📷 Capture Fingerprint", None))
        self.predictionResultBrowser.setHtml(QCoreApplication.translate("MainWindow", u"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">
p, li { white-space: pre-wrap; }
hr { height: 1px; border-width: 0; }
li.unchecked::marker { content: "\\2610"; }
li.checked::marker { content: "\\2612"; }
</style></head><body style=" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;">
<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:12pt; font-weight:700; color:#ffffff;">🤖 AI Model Prediction: [Waiting for capture...]</span></p>
<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:11pt; color:#d1d5db;">Do you agree with the AI prediction?</span></p></body></html>""", None))
        
        # Prediction response buttons
        self.agreeButton.setText(QCoreApplication.translate("MainWindow", u"✅ Yes, I Agree", None))
        self.disagreeButton.setText(QCoreApplication.translate("MainWindow", u"❌ No, I Disagree", None))
        
        # Manual pattern selection
        self.manualPatternLabel.setText(QCoreApplication.translate("MainWindow", u"Select the correct pattern:", None))
        
        # Action buttons
        self.saveCurrentFingerButton.setText(QCoreApplication.translate("MainWindow", u"💾 Save Current Finger", None))
        self.nextFingerButton.setText(QCoreApplication.translate("MainWindow", u"➡️ Next Finger", None))
        self.retakeCurrentButton.setText(QCoreApplication.translate("MainWindow", u"🔄 Retake Current", None))
        
        # Captured fingers section
        self.capturedFingersHeader.setHtml(QCoreApplication.translate("MainWindow", u"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">
p, li { white-space: pre-wrap; }
hr { height: 1px; border-width: 0; }
li.unchecked::marker { content: "\\2610"; }
li.checked::marker { content: "\\2612"; }
</style></head><body style=" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;">
<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:16pt; font-weight:700; color:#ffffff;">📋 Captured Fingerprints Summary</span></p></body></html>""", None))
        
        self.capturedFingersListLabel.setText(QCoreApplication.translate("MainWindow", u"No fingerprints captured yet. Start by selecting a finger and capturing its print above.", None))
        
        # Final action buttons
        self.saveAllDataButton.setText(QCoreApplication.translate("MainWindow", u"💾 Save Complete Patient Data", None))
        self.clearAllDataButton.setText(QCoreApplication.translate("MainWindow", u"🗑️ Clear All Data", None))