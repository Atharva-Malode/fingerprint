from PySide6.QtCore import QTimer, QObject, Qt
from PySide6.QtGui import QPixmap, QImage
from .fingerprint_device import FingerprintDevice
# from utils.image_utils import save_image
from utils.save_image import save_image

class FingerprintCaptureController(QObject):
    def __init__(self, image_label):
        super().__init__()
        self.label = image_label
        self.device = FingerprintDevice()
        self.preview_timer = QTimer()
        self.preview_timer.timeout.connect(self._capture_frame)
        self.current_image = None

    def start_preview(self):
        if self.device.initialize():
            self.preview_timer.start(100)
            self.label.setText("")
            return True
        else:
            self.label.setText("❌ Scanner Initialization Failed")
            return False

    def stop_preview(self):
        self.preview_timer.stop()
        self.label.setText("Preview stopped. Click 'Start Preview' to resume.")
        self.label.setAlignment(Qt.AlignCenter)

    def _capture_frame(self):
        img = self.device.capture_frame()
        if img is not None:
            self.current_image = img.copy()
            h, w = img.shape
            qimage = QImage(img.data, w, h, w, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qimage)
            self.label.setPixmap(pixmap.scaled(
                self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def capture_and_save_image(self):
        if self.current_image is not None:
            return save_image(self.current_image)
        return None

    def cleanup(self):
        self.stop_preview()
        self.device.terminate()
