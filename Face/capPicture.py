import os
import cv2
import numpy as np
from mtcnn.mtcnn import MTCNN
from sklearn.model_selection import train_test_split

# Function to capture 30 images from the webcam
def capture_images(name, save_dir='dataset_split'):
    # Create directories if not exist
    train_dir = os.path.join(save_dir, 'train', name)
    val_dir = os.path.join(save_dir, 'val', name)
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    detector = MTCNN()
    img_count = 0
    captured_images = []

    print("Press 'c' to capture image. Press 'q' to quit.")
    while img_count < 30:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Display the frame
        cv2.imshow('Capturing Images', frame)
        
        # Check for key press
        key = cv2.waitKey(1)
        if key & 0xFF == ord('c'):
            results = detector.detect_faces(frame)
            if results:
                x1, y1, width, height = results[0]['box']
                x1, y1 = abs(x1), abs(y1)
                x2, y2 = x1 + width, y1 + height
                face = frame[y1:y2, x1:x2]
                face = cv2.resize(face, (160, 160))
                captured_images.append(face)
                img_count += 1
                print(f"Captured image {img_count}")
        elif key & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    # Split the images into training and validation sets
    train_images, val_images = train_test_split(captured_images, test_size=0.33, random_state=42)
    
    # Save images
    for i, img in enumerate(train_images):
        cv2.imwrite(os.path.join(train_dir, f'{name}_{i+1}.jpg'), img)
    for i, img in enumerate(val_images):
        cv2.imwrite(os.path.join(val_dir, f'{name}_{i+1}.jpg'), img)

# Main function
def main():
    # Input name
    name = input("Enter your name: ")
    
    # Capture images
    capture_images(name)

    print("Images captured and saved successfully.")

if __name__ == "__main__":
    main()
