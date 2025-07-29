# core/fingerprint_capture.py
import ctypes
from ctypes import c_ulong, byref, create_string_buffer
import numpy as np
import os
import cv2
from datetime import datetime
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer, QObject, Signal, Qt

# SDK Constants
FTR_RETCODE_OK = 0
FTR_PARAM_IMAGE_WIDTH = 1
FTR_PARAM_IMAGE_HEIGHT = 2
FTR_PARAM_IMAGE_SIZE = 3
FTR_PARAM_CB_FRAME_SOURCE = 4
FSD_FUTRONIC_USB = 1
DWORD = c_ulong

class FingerprintScanner(QObject):
    """Simple fingerprint scanner with manual start/stop"""
    
    def __init__(self, image_label):
        super().__init__()
        self.label = image_label
        self.ftr = None
        
        # Timer for live preview
        self.preview_timer = QTimer()
        self.preview_timer.timeout.connect(self._capture_frame)
        
        # Scanner state
        self.width = 0
        self.height = 0
        self.image_size = 0
        self.buffer = None
        self.is_initialized = False
        self.is_previewing = False
        self.current_image = None
        
        # Create data folder
        self.data_folder = "data"
        os.makedirs(self.data_folder, exist_ok=True)
        
        # Set initial placeholder
        self.label.setText("Click 'Start Preview' to begin")
        self.label.setAlignment(Qt.AlignCenter)
    
    def initialize_scanner(self):
        """Initialize scanner when needed"""
        if self.is_initialized:
            return True
        
        try:
            print("🔍 Initializing fingerprint scanner...")
            
            # Load DLL
            self.ftr = ctypes.WinDLL("FTRAPI.dll")
            
            # Initialize
            ret = self.ftr.FTRInitialize()
            if ret != FTR_RETCODE_OK:
                print(f"❌ FTRInitialize failed: {ret}")
                return False
            
            # Set USB source
            self.ftr.FTRSetParam(FTR_PARAM_CB_FRAME_SOURCE, FSD_FUTRONIC_USB)
            
            # Get image parameters
            width, height, size = DWORD(), DWORD(), DWORD()
            self.ftr.FTRGetParam(FTR_PARAM_IMAGE_WIDTH, byref(width))
            self.ftr.FTRGetParam(FTR_PARAM_IMAGE_HEIGHT, byref(height))
            self.ftr.FTRGetParam(FTR_PARAM_IMAGE_SIZE, byref(size))
            
            self.width = width.value
            self.height = height.value
            self.image_size = size.value
            
            if self.width == 0 or self.height == 0:
                print("❌ Invalid image dimensions")
                return False
            
            print(f"✅ Scanner initialized: {self.width}x{self.height}")
            
            # Create buffer
            self.buffer = create_string_buffer(self.image_size)
            self.is_initialized = True
            return True
            
        except Exception as e:
            print(f"❌ Scanner initialization failed: {e}")
            return False
    
    def start_preview(self):
        """Start live preview"""
        if not self.initialize_scanner():
            self.label.setText("❌ Scanner Error - Check Connection")
            return False
        
        print("📸 Starting live preview...")
        self.is_previewing = True
        self.label.setText("")
        self.preview_timer.start(100)  # Update every 100ms
        return True
    
    def stop_preview(self):
        """Stop live preview"""
        print("⏹️ Stopping preview...")
        self.is_previewing = False
        self.preview_timer.stop()
        self.label.setText("Preview stopped. Click 'Start Preview' to resume.")
        self.label.setAlignment(Qt.AlignCenter)
    
    def _capture_frame(self):
        """Capture single frame for preview"""
        if not self.is_initialized:
            return
        
        try:
            ret = self.ftr.FTRCaptureFrame(None, self.buffer)
            
            if ret == FTR_RETCODE_OK:
                # Convert to numpy array
                img_array = np.frombuffer(self.buffer.raw, dtype=np.uint8)
                img_array = img_array.reshape((self.height, self.width))
                
                # Store current image for capture
                self.current_image = img_array.copy()
                
                # Update display
                self._update_display(img_array)
            
        except Exception as e:
            print(f"⚠️ Frame capture error: {e}")
    
    def _update_display(self, img_array):
        """Update the display with captured image"""
        try:
            h, w = img_array.shape
            
            # Create QImage
            qimage = QImage(img_array.data, w, h, w, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qimage)
            
            # Scale to fit label
            scaled_pixmap = pixmap.scaled(
                self.label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            self.label.setPixmap(scaled_pixmap)
            
        except Exception as e:
            print(f"❌ Display update error: {e}")
    
    def capture_and_save_image(self):
        """Capture current image and save to data folder"""
        if not self.current_image is None:
            try:
                # Generate filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"fingerprint_{timestamp}.png"
                filepath = os.path.join(self.data_folder, filename)
                
                # Save image using OpenCV
                cv2.imwrite(filepath, self.current_image)
                
                print(f"✅ Image saved: {filepath}")
                return filepath
                
            except Exception as e:
                print(f"❌ Save failed: {e}")
                return None
        else:
            print("❌ No image to save - start preview first")
            return None
    
    def cleanup(self):
        """Clean up resources"""
        print("🧹 Cleaning up scanner...")
        self.stop_preview()
        
        if self.ftr and self.is_initialized:
            try:
                self.ftr.FTRTerminate()
                print("✅ Scanner terminated")
            except Exception as e:
                print(f"⚠️ Cleanup error: {e}")

