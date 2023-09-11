import cv2
import threading

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)  # 0 for default camera
        self.frame = None
        self.lock = threading.Lock()
        self.is_running = True

        # Start the capture thread
        self.thread = threading.Thread(target=self._capture_loop)
        self.thread.start()

    def _capture_loop(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            with self.lock:
                self.frame = frame

    def get_latest_frame(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        self.is_running = False
        self.thread.join()
        self.cap.release()

# Example usage:
camera = Camera()

try:
    while True:
        # Call this function whenever you need the latest image
        img = camera.get_latest_frame()
        if img is not None:
            cv2.imshow('Latest Frame', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
finally:
    camera.stop()
    cv2.destroyAllWindows()
