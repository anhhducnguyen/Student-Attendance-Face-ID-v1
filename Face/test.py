import cv2
from numpy import expand_dims
from sklearn.preprocessing import LabelEncoder, Normalizer
from sklearn.svm import SVC
from matplotlib import pyplot as plt
from numpy import load
from mtcnn.mtcnn import MTCNN
from keras_facenet import FaceNet
import numpy as np

# Function to load data and preprocess it
def load_and_preprocess_data():
    # Load faces
    data = load('5-celebrity-faces-dataset.npz')
    testX_faces = data['arr_2']
    # Load face embeddings
    data = load('5-celebrity-faces-embeddings.npz')
    trainX, trainy, testX, testy = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']
    
    # Normalize input vectors
    in_encoder = Normalizer(norm='l2')
    trainX = in_encoder.transform(trainX)
    testX = in_encoder.transform(testX)
    
    # Label encode targets
    out_encoder = LabelEncoder()
    out_encoder.fit(trainy)
    trainy = out_encoder.transform(trainy)
    testy = out_encoder.transform(testy)
    
    return trainX, trainy, testX, testy, testX_faces, out_encoder

# Function to train the SVM classifier
def train_classifier(trainX, trainy):
    model = SVC(kernel='linear', probability=True)
    model.fit(trainX, trainy)
    return model

embedder = FaceNet()

# Load FaceNet model for embedding extraction
facenet_model = embedder.model  # Make sure you have the FaceNet model file
detector = MTCNN()

# Function to extract face embeddings from a given frame
def get_face_embeddings(frame):
    faces = detector.detect_faces(frame)
    embeddings = []
    boxes = []
    for face in faces:
        # Extract the bounding box
        x1, y1, width, height = face['box']
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        face_pixels = frame[y1:y2, x1:x2]
        face_pixels = cv2.resize(face_pixels, (160, 160))
        face_pixels = face_pixels.astype('float32')
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
        samples = expand_dims(face_pixels, axis=0)
        yhat = facenet_model.predict(samples)
        embeddings.append(yhat[0])
        boxes.append((x1, y1, x2, y2))
    return embeddings, boxes

# Function to capture video from the webcam and make predictions
def realtime_face_recognition(model, out_encoder):
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        face_embeddings, boxes = get_face_embeddings(frame)
        
        for i, face_emb in enumerate(face_embeddings):
            samples = expand_dims(face_emb, axis=0)
            yhat_class = model.predict(samples)
            yhat_prob = model.predict_proba(samples)
            class_index = yhat_class[0]
            class_probability = yhat_prob[0, class_index] * 100
            predict_name = out_encoder.inverse_transform(yhat_class)[0]
            
            # Extract bounding box
            x1, y1, x2, y2 = boxes[i]
            
            # Display the name and probability on the frame
            cv2.putText(frame, f'{predict_name} ({class_probability:.2f}%)', 
                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Display the resulting frame
        cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def main():
    trainX, trainy, testX, testy, testX_faces, out_encoder = load_and_preprocess_data()
    model = train_classifier(trainX, trainy)
    realtime_face_recognition(model, out_encoder)

if __name__ == "__main__":
    main()
