class FaceDetector:
    """Abstract base class for face detection implementations"""
    
    def detect(self, frame):
        """
        Detect faces in a frame.
        
        Args:
            frame: OpenCV image (numpy array)
            
        Returns:
            List of tuples: [(x, y, width, height, confidence), ...]
        """
        raise NotImplementedError("Subclasses must implement detect()")
