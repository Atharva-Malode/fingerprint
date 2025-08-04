import ctypes
from ctypes import c_ulong, byref, create_string_buffer
import numpy as np
from .constant import FTR_RETCODE_OK, FTR_PARAM_IMAGE_WIDTH, FTR_PARAM_IMAGE_HEIGHT, FTR_PARAM_IMAGE_SIZE, FTR_PARAM_CB_FRAME_SOURCE, FSD_FUTRONIC_USB

DWORD = c_ulong

class FingerprintDevice:
    def __init__(self):
        self.ftr = None
        self.width = 0
        self.height = 0
        self.image_size = 0
        self.buffer = None
        self.initialized = False

    def initialize(self):
        try:
            self.ftr = ctypes.WinDLL("FTRAPI.dll")
            if self.ftr.FTRInitialize() != FTR_RETCODE_OK:
                print("❌ FTRInitialize failed")
                return False

            self.ftr.FTRSetParam(FTR_PARAM_CB_FRAME_SOURCE, FSD_FUTRONIC_USB)

            width, height, size = DWORD(), DWORD(), DWORD()
            self.ftr.FTRGetParam(FTR_PARAM_IMAGE_WIDTH, byref(width))
            self.ftr.FTRGetParam(FTR_PARAM_IMAGE_HEIGHT, byref(height))
            self.ftr.FTRGetParam(FTR_PARAM_IMAGE_SIZE, byref(size))

            self.width = width.value
            self.height = height.value
            self.image_size = size.value

            self.buffer = create_string_buffer(self.image_size)
            self.initialized = True
            return True

        except Exception as e:
            print(f"❌ Initialization error: {e}")
            return False

    def capture_frame(self):
        if not self.initialized:
            return None

        ret = self.ftr.FTRCaptureFrame(None, self.buffer)
        if ret == FTR_RETCODE_OK:
            img_array = np.frombuffer(self.buffer.raw, dtype=np.uint8)
            return img_array.reshape((self.height, self.width))
        else:
            print("⚠️ Capture failed")
            return None

    def terminate(self):
        if self.ftr and self.initialized:
            self.ftr.FTRTerminate()
            self.initialized = False