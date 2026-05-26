import cv2
import dlib
import numpy as np
from PIL import Image

class InputProcessor:
    def __init__(self, shape_predictor_path):
        """Initialize the face detector and shape predictor"""
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(shape_predictor_path)

    def detect_and_align(self, image_path):
        """Detect face and align it for better animation results"""
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not read image file")
        
        # Convert to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        faces = self.detector(img_rgb)
        if len(faces) == 0:
            raise ValueError("No face detected in the image")
        
        # Get the largest face
        face = max(faces, key=lambda rect: rect.width() * rect.height())
        
        # Get facial landmarks
        landmarks = self.predictor(img_rgb, face)
        
        # Convert landmarks to numpy array
        landmarks_points = np.array([[p.x, p.y] for p in landmarks.parts()])
        
        # Calculate face center and size
        face_center = np.mean(landmarks_points, axis=0).astype(int)
        face_size = max(face.width(), face.height())
        
        # Add margin (30% of face size)
        margin = int(face_size * 0.3)
        
        # Calculate crop boundaries
        x1 = max(0, face_center[0] - face_size//2 - margin)
        y1 = max(0, face_center[1] - face_size//2 - margin)
        x2 = min(img.shape[1], face_center[0] + face_size//2 + margin)
        y2 = min(img.shape[0], face_center[1] + face_size//2 + margin)
        
        # Crop image
        cropped_face = img_rgb[y1:y2, x1:x2]
        
        # Resize to a standard size (512x512)
        resized_face = cv2.resize(cropped_face, (512, 512))
        
        return resized_face

    def process_text(self, text_path):
        """Process the input text script"""
        try:
            with open(text_path, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            
            # Basic text cleaning
            text = ' '.join(text.split())  # Remove extra whitespace
            
            if not text:
                raise ValueError("Empty text script")
                
            return text
            
        except Exception as e:
            raise ValueError(f"Error processing text file: {str(e)}")
