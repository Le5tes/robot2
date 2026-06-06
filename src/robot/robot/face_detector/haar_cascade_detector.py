
from robot.face_detector.face_detector import FaceDetector
import cv2


class HaarCascadeDetector(FaceDetector):
    """Face detector using OpenCV Haar Cascades"""
    
    def __init__(self, cascade_path=None):
        """
        Initialize Haar cascade detector.
        
        Args:
            cascade_path: Path to Haar cascade XML file.
                         If None, uses OpenCV's default frontal face cascade.
        """
        if cascade_path is None:
            # Use OpenCV's built-in cascade
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if self.face_cascade.empty():
            raise RuntimeError(f"Failed to load Haar cascade from {cascade_path}")
    
    def detect(self, frame):
        """
        Detect faces using Haar cascades.
        
        Args:
            frame: OpenCV image (BGR or grayscale)
            
        Returns:
            List of tuples: [(x, y, width, height, confidence), ...]
        """
        # Convert to grayscale if needed
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Convert to list of tuples with confidence
        # Haar cascades don't provide confidence, so we use 1.0
        detections = [(int(x), int(y), int(w), int(h), 1.0) 
                     for (x, y, w, h) in faces]
        
        return detections
