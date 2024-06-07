# import cv2
# from django.http import HttpResponse
# from django.shortcuts import render
# from numpy import expand_dims
# from sklearn.preprocessing import LabelEncoder, Normalizer
# from sklearn.svm import SVC
# from matplotlib import pyplot as plt
# from numpy import load
# from mtcnn.mtcnn import MTCNN
# from keras_facenet import FaceNet
# import numpy as np

# # Function to load data and preprocess it
# def load_and_preprocess_data():
#     # Load faces
#     data = load('Face/5-celebrity-faces-dataset.npz')
#     testX_faces = data['arr_2']
#     # Load face embeddings
#     data = load('Face/5-celebrity-faces-embeddings.npz')
#     trainX, trainy, testX, testy = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']
    
#     # Normalize input vectors
#     in_encoder = Normalizer(norm='l2')
#     trainX = in_encoder.transform(trainX)
#     testX = in_encoder.transform(testX)
    
#     # Label encode targets
#     out_encoder = LabelEncoder()
#     out_encoder.fit(trainy)
#     trainy = out_encoder.transform(trainy)
#     testy = out_encoder.transform(testy)
    
#     return trainX, trainy, testX, testy, testX_faces, out_encoder

# # Function to train the SVM classifier
# def train_classifier(trainX, trainy):
#     model = SVC(kernel='linear', probability=True)
#     model.fit(trainX, trainy)
#     return model

# embedder = FaceNet()

# # Load FaceNet model for embedding extraction
# facenet_model = embedder.model  # Make sure you have the FaceNet model file
# detector = MTCNN()

# # Function to extract face embeddings from a given frame
# def get_face_embeddings(frame):
#     faces = detector.detect_faces(frame)
#     embeddings = []
#     boxes = []
#     for face in faces:
#         # Extract the bounding box
#         x1, y1, width, height = face['box']
#         x1, y1 = abs(x1), abs(y1)
#         x2, y2 = x1 + width, y1 + height
#         face_pixels = frame[y1:y2, x1:x2]
#         face_pixels = cv2.resize(face_pixels, (160, 160))
#         face_pixels = face_pixels.astype('float32')
#         mean, std = face_pixels.mean(), face_pixels.std()
#         face_pixels = (face_pixels - mean) / std
#         samples = expand_dims(face_pixels, axis=0)
#         yhat = facenet_model.predict(samples)
#         embeddings.append(yhat[0])
#         boxes.append((x1, y1, x2, y2))
#     return embeddings, boxes

# # Function to capture video from the webcam and make predictions
# def realtime_face_recognition(model, out_encoder):
#     cap = cv2.VideoCapture(0)
    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         face_embeddings, boxes = get_face_embeddings(frame)
        
#         for i, face_emb in enumerate(face_embeddings):
#             samples = expand_dims(face_emb, axis=0)
#             yhat_class = model.predict(samples)
#             yhat_prob = model.predict_proba(samples)
#             class_index = yhat_class[0]
#             class_probability = yhat_prob[0, class_index] * 100
#             predict_name = out_encoder.inverse_transform(yhat_class)[0]
            
#             # Extract bounding box
#             x1, y1, x2, y2 = boxes[i]
            
#             # Display the name and probability on the frame
#             cv2.putText(frame, f'{predict_name} ({class_probability:.2f}%)', 
#                         (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
#         # Display the resulting frame
#         cv2.imshow('Video', frame)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
    
#     cap.release()
#     cv2.destroyAllWindows()

# def diemdanh(request):
#     trainX, trainy, testX, testy, testX_faces, out_encoder = load_and_preprocess_data()
#     model = train_classifier(trainX, trainy)
#     realtime_face_recognition(model, out_encoder)
#     # return HttpResponse("Điểm danh thành công.")
#     return render(request, 'admin/your_template.html', {'success_message': "Điểm danh thành công."})

# if __name__ == "__main__":
#     diemdanh()



# import cv2
# from django.shortcuts import render
# from numpy import expand_dims
# from sklearn.preprocessing import LabelEncoder, Normalizer
# from sklearn.svm import SVC
# from numpy import load
# from mtcnn.mtcnn import MTCNN
# from keras_facenet import FaceNet
# import numpy as np
# from datetime import datetime  # Import datetime for current date and time
# from .models import TblStudents, Attendance

# # Function to load data and preprocess it
# def load_and_preprocess_data():
#     # Load faces
#     data = load('Face/5-celebrity-faces-dataset.npz')
#     testX_faces = data['arr_2']
#     # Load face embeddings
#     data = load('Face/5-celebrity-faces-embeddings.npz')
#     trainX, trainy, testX, testy = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']
    
#     # Normalize input vectors
#     in_encoder = Normalizer(norm='l2')
#     trainX = in_encoder.transform(trainX)
#     testX = in_encoder.transform(testX)
    
#     # Label encode targets
#     out_encoder = LabelEncoder()
#     out_encoder.fit(trainy)
#     trainy = out_encoder.transform(trainy)
#     testy = out_encoder.transform(testy)
    
#     return trainX, trainy, testX, testy, testX_faces, out_encoder

# def train_classifier(trainX, trainy):
#     model = SVC(kernel='linear', probability=True)
#     model.fit(trainX, trainy)
#     return model

# embedder = FaceNet()
# facenet_model = embedder.model
# detector = MTCNN()

# def get_face_embeddings(frame):
#     faces = detector.detect_faces(frame)
#     embeddings = []
#     boxes = []
#     for face in faces:
#         x1, y1, width, height = face['box']
#         x1, y1 = abs(x1), abs(y1)
#         x2, y2 = x1 + width, y1 + height
#         face_pixels = frame[y1:y2, x1:x2]
#         face_pixels = cv2.resize(face_pixels, (160, 160))
#         face_pixels = face_pixels.astype('float32')
#         mean, std = face_pixels.mean(), face_pixels.std()
#         face_pixels = (face_pixels - mean) / std
#         samples = expand_dims(face_pixels, axis=0)
#         yhat = facenet_model.predict(samples)
#         embeddings.append(yhat[0])
#         boxes.append((x1, y1, x2, y2))
#     return embeddings, boxes

# def realtime_face_recognition(model, out_encoder):
#     cap = cv2.VideoCapture(0)
#     confidence_threshold = 70.0  # Confidence threshold
#     attendance_message = ""  # Variable to store attendance message
    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         face_embeddings, boxes = get_face_embeddings(frame)
        
#         for i, face_emb in enumerate(face_embeddings):
#             samples = expand_dims(face_emb, axis=0)
#             yhat_class = model.predict(samples)
#             yhat_prob = model.predict_proba(samples)
#             class_index = yhat_class[0]
#             class_probability = yhat_prob[0, class_index] * 100
#             predict_name = out_encoder.inverse_transform(yhat_class)[0]
            
#             x1, y1, x2, y2 = boxes[i]
            
#             cv2.putText(frame, f'{predict_name} ({class_probability:.2f}%)', 
#                         (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
#             # Strip any prefix from the predicted name
#             stripped_name = predict_name.split('_', 1)[-1]
#             print(f"Detected: {stripped_name} with {class_probability:.2f}% confidence")  # Debugging info
            
#             if class_probability >= confidence_threshold:
#                 try:
#                     student = TblStudents.objects.get(name=stripped_name)
#                     print(f"Marking attendance for {stripped_name}")  # Debugging info
#                     Attendance.objects.update_or_create(
#                         student=student,
#                         datetime=datetime.now(),  # Save current datetime
#                         defaults={'attended': True}
#                     )
#                     attendance_message = f"{student.student_id} - {student.name} Attendance successfully"
#                     print(attendance_message)  # Debugging info
#                 except TblStudents.DoesNotExist:
#                     print(f"Student {stripped_name} not found in database")  # Debugging info
        
#         if attendance_message:
#             cv2.putText(frame, attendance_message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
#         cv2.imshow('Video', frame)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
    
#     cap.release()
#     cv2.destroyAllWindows()

# def diemdanh(request):
#     trainX, trainy, testX, testy, testX_faces, out_encoder = load_and_preprocess_data()
#     model = train_classifier(trainX, trainy)
#     realtime_face_recognition(model, out_encoder)
#     return render(request, 'admin/your_template.html', {'success_message': "Điểm danh thành công."})


# import cv2
# from django.shortcuts import render
# from numpy import expand_dims
# from sklearn.preprocessing import LabelEncoder, Normalizer
# from sklearn.svm import SVC
# from numpy import load
# from mtcnn.mtcnn import MTCNN
# from keras_facenet import FaceNet
# import numpy as np
# from datetime import datetime
# import pytz  # Import pytz for timezone handling
# from .models import TblStudents, Attendance

# # Function to load data and preprocess it
# def load_and_preprocess_data():
#     # Load faces
#     data = load('Face/5-celebrity-faces-dataset.npz')
#     testX_faces = data['arr_2']
#     # Load face embeddings
#     data = load('Face/5-celebrity-faces-embeddings.npz')
#     trainX, trainy, testX, testy = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']
    
#     # Normalize input vectors
#     in_encoder = Normalizer(norm='l2')
#     trainX = in_encoder.transform(trainX)
#     testX = in_encoder.transform(testX)
    
#     # Label encode targets
#     out_encoder = LabelEncoder()
#     out_encoder.fit(trainy)
#     trainy = out_encoder.transform(trainy)
#     testy = out_encoder.transform(testy)
    
#     return trainX, trainy, testX, testy, testX_faces, out_encoder

# def train_classifier(trainX, trainy):
#     model = SVC(kernel='linear', probability=True)
#     model.fit(trainX, trainy)
#     return model

# embedder = FaceNet()
# facenet_model = embedder.model
# detector = MTCNN()

# def get_face_embeddings(frame):
#     faces = detector.detect_faces(frame)
#     embeddings = []
#     boxes = []
#     for face in faces:
#         x1, y1, width, height = face['box']
#         x1, y1 = abs(x1), abs(y1)
#         x2, y2 = x1 + width, y1 + height
#         face_pixels = frame[y1:y2, x1:x2]
#         face_pixels = cv2.resize(face_pixels, (160, 160))
#         face_pixels = face_pixels.astype('float32')
#         mean, std = face_pixels.mean(), face_pixels.std()
#         face_pixels = (face_pixels - mean) / std
#         samples = expand_dims(face_pixels, axis=0)
#         yhat = facenet_model.predict(samples)
#         embeddings.append(yhat[0])
#         boxes.append((x1, y1, x2, y2))
#     return embeddings, boxes

# def realtime_face_recognition(model, out_encoder):
#     cap = cv2.VideoCapture(0)
#     attendance_marked = False  # Biến để kiểm tra xem đã đánh dấu điểm danh hay chưa
#     confidence_threshold = 70.0  # Ngưỡng tin cậy
#     attendance_message = ""  # Biến lưu thông báo điểm danh
    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         face_embeddings, boxes = get_face_embeddings(frame)
        
#         for i, face_emb in enumerate(face_embeddings):
#             samples = expand_dims(face_emb, axis=0)
#             yhat_class = model.predict(samples)
#             yhat_prob = model.predict_proba(samples)
#             class_index = yhat_class[0]
#             class_probability = yhat_prob[0, class_index] * 100
#             predict_name = out_encoder.inverse_transform(yhat_class)[0]
            
#             x1, y1, x2, y2 = boxes[i]
            
#             cv2.putText(frame, f'{predict_name} ({class_probability:.2f}%)', 
#                         (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
#             # Strip any prefix from the predicted name
#             stripped_name = predict_name.split('_', 1)[-1]
#             print(f"Detected: {stripped_name} with {class_probability:.2f}% confidence")  # Debugging info
            
#             if class_probability >= confidence_threshold and not attendance_marked:
#                 try:
#                     student = TblStudents.objects.get(name=stripped_name)
#                     print(f"Marking attendance for {stripped_name}")  # Debugging info
                    
#                     # Get the current time in Vietnam timezone
#                     vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
#                     current_time_vn = datetime.now(vn_tz)
                    
#                     Attendance.objects.update_or_create(
#                         student=student,
#                         datetime=current_time_vn,
#                         defaults={'attended': True}
#                     )
#                     attendance_marked = True  # Đánh dấu điểm danh đã được thực hiện
#                     attendance_message = f"{student.student_id} - {student.name} Attendance successfully"
#                     print(attendance_message)  # Debugging info
#                 except TblStudents.DoesNotExist:
#                     print(f"Student {stripped_name} not found in database")  # Debugging info
        
#         if attendance_message:
#             cv2.putText(frame, attendance_message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
#         cv2.imshow('Video', frame)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
    
#     cap.release()
#     cv2.destroyAllWindows()

# def diemdanh(request):
#     trainX, trainy, testX, testy, testX_faces, out_encoder = load_and_preprocess_data()
#     model = train_classifier(trainX, trainy)
#     realtime_face_recognition(model, out_encoder)
#     return render(request, 'admin/your_template.html', {'success_message': "Điểm danh thành công."})



# import cv2
# from django.shortcuts import render
# from numpy import expand_dims
# from mtcnn.mtcnn import MTCNN
# from keras_facenet import FaceNet
# import pickle

# # Load FaceNet model for embedding extraction
# embedder = FaceNet()
# facenet_model = embedder.model
# detector = MTCNN()

# # Extract face embeddings from a given frame
# def get_face_embeddings(frame):
#     faces = detector.detect_faces(frame)
#     embeddings = []
#     boxes = []
#     for face in faces:
#         x1, y1, width, height = face['box']
#         x1, y1 = abs(x1), abs(y1)
#         x2, y2 = x1 + width, y1 + height
#         face_pixels = frame[y1:y2, x1:x2]
#         face_pixels = cv2.resize(face_pixels, (160, 160))
#         face_pixels = face_pixels.astype('float32')
#         mean, std = face_pixels.mean(), face_pixels.std()
#         face_pixels = (face_pixels - mean) / std
#         samples = expand_dims(face_pixels, axis=0)
#         yhat = facenet_model.predict(samples)
#         embeddings.append(yhat[0])
#         boxes.append((x1, y1, x2, y2))
#     return embeddings, boxes

# # Capture video from the webcam and make predictions
# def realtime_face_recognition(model, out_encoder):
#     cap = cv2.VideoCapture(0)
    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         frame = cv2.flip(frame, 1)

#         face_embeddings, boxes = get_face_embeddings(frame)
        
#         for i, face_emb in enumerate(face_embeddings):
#             samples = expand_dims(face_emb, axis=0)
#             yhat_class = model.predict(samples)
#             yhat_prob = model.predict_proba(samples)
#             class_index = yhat_class[0]
#             class_probability = yhat_prob[0, class_index] * 100
#             predict_name = out_encoder.inverse_transform(yhat_class)[0]
            
#             x1, y1, x2, y2 = boxes[i]
#             cv2.putText(frame, f'{predict_name} ({class_probability:.2f}%)', 
#                         (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             stripped_name = predict_name.split('_', 1)[-1]
#             print(f"Detected: {stripped_name} with {class_probability:.2f}% confidence")
        
#         cv2.imshow('Video', frame)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
    
#     cap.release()
#     cv2.destroyAllWindows()

# def diemdanh(request):
#     with open('Face/svm_model/svm_model.pkl', 'rb') as model_file:
#         model = pickle.load(model_file)
#     with open('Face/svm_model/out_encoder.pkl', 'rb') as encoder_file:
#         out_encoder = pickle.load(encoder_file)

#     realtime_face_recognition(model, out_encoder)
#     return render(request, 'admin/your_template.html', {'success_message': "Điểm danh thành công."})

# import cv2
# from django.shortcuts import render
# from numpy import expand_dims
# from mtcnn.mtcnn import MTCNN
# from keras_facenet import FaceNet
# import pickle
# import json

# # Load FaceNet model for embedding extraction
# embedder = FaceNet()
# facenet_model = embedder.model
# detector = MTCNN()

# # Extract face embeddings from a given frame
# def get_face_embeddings(frame):
#     faces = detector.detect_faces(frame)
#     embeddings = []
#     boxes = []
#     for face in faces:
#         x1, y1, width, height = face['box']
#         x1, y1 = abs(x1), abs(y1)
#         x2, y2 = x1 + width, y1 + height
#         face_pixels = frame[y1:y2, x1:x2]
#         face_pixels = cv2.resize(face_pixels, (160, 160))
#         face_pixels = face_pixels.astype('float32')
#         mean, std = face_pixels.mean(), face_pixels.std()
#         face_pixels = (face_pixels - mean) / std
#         samples = expand_dims(face_pixels, axis=0)
#         yhat = facenet_model.predict(samples)
#         embeddings.append(yhat[0])
#         boxes.append((x1, y1, x2, y2))
#     return embeddings, boxes

# # Capture video from the webcam and make predictions
# def realtime_face_recognition(model, out_encoder):
#     cap = cv2.VideoCapture(0)
#     detections = []  # List to store detection information
    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         frame = cv2.flip(frame, 1)

#         face_embeddings, boxes = get_face_embeddings(frame)
        
#         for i, face_emb in enumerate(face_embeddings):
#             samples = expand_dims(face_emb, axis=0)
#             yhat_class = model.predict(samples)
#             yhat_prob = model.predict_proba(samples)
#             class_index = yhat_class[0]
#             class_probability = yhat_prob[0, class_index] * 100
#             predict_name = out_encoder.inverse_transform(yhat_class)[0]
            
#             x1, y1, x2, y2 = boxes[i]
#             cv2.putText(frame, f'{predict_name} ({class_probability:.2f}%)', 
#                         (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
#             # In thông báo nhận diện khuôn mặt
#             stripped_name = predict_name.split('_', 1)[-1]
#             print(f"Detected: {stripped_name} with {class_probability:.2f}% confidence")
            
#             # Lưu thông tin nhận diện vào danh sách
#             detection_info = {
#                 'name': stripped_name,
#                 'confidence': class_probability,
#                 'box': {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
#             }
#             detections.append(detection_info)
        
#         cv2.imshow('Video', frame)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
    
#     cap.release()
#     cv2.destroyAllWindows()
    
#     # Ghi thông tin nhận diện ra file JSON
#     with open('detections.json', 'w') as json_file:
#         json.dump(detections, json_file, indent=4)

# def diemdanh(request):
#     with open('Face/svm_model/svm_model.pkl', 'rb') as model_file:
#         model = pickle.load(model_file)
#     with open('Face/svm_model/out_encoder.pkl', 'rb') as encoder_file:
#         out_encoder = pickle.load(encoder_file)

#     realtime_face_recognition(model, out_encoder)
#     return render(request, 'admin/your_template.html', {'success_message': "Điểm danh thành công."})
















import cv2
from django.shortcuts import render
from numpy import expand_dims
from mtcnn.mtcnn import MTCNN
from keras_facenet import FaceNet
import pickle
import json
from datetime import datetime
from .models import TblStudents, Attendance

# Load FaceNet model for embedding extraction
embedder = FaceNet()
facenet_model = embedder.model
detector = MTCNN()

# Extract face embeddings from a given frame
def get_face_embeddings(frame):
    faces = detector.detect_faces(frame)
    embeddings = []
    boxes = []
    for face in faces:
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

# Capture video from the webcam and make predictions
def realtime_face_recognition(model, out_encoder):
    cap = cv2.VideoCapture(0)
    detections = []  # List to store detection information
    confidence_threshold = 70.0  # Confidence threshold
    attendance_message = ""  # Variable to store attendance message
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)

        face_embeddings, boxes = get_face_embeddings(frame)
        
        for i, face_emb in enumerate(face_embeddings):
            samples = expand_dims(face_emb, axis=0)
            yhat_class = model.predict(samples)
            yhat_prob = model.predict_proba(samples)
            class_index = yhat_class[0]
            class_probability = yhat_prob[0, class_index] * 100
            predict_name = out_encoder.inverse_transform(yhat_class)[0]
            
            x1, y1, x2, y2 = boxes[i]
            cv2.putText(frame, f'{predict_name} ({class_probability:.2f}%)', 
                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # In thông báo nhận diện khuôn mặt
            stripped_name = predict_name.split('_', 1)[-1]
            print(f"Detected: {stripped_name} with {class_probability:.2f}% confidence")
            
            if class_probability >= confidence_threshold:
                try:
                    student = TblStudents.objects.get(name=stripped_name)
                    print(f"Marking attendance for {stripped_name}")
                    Attendance.objects.update_or_create(
                        student=student,
                        datetime=datetime.now(),
                        defaults={'attended': True}
                    )
                    attendance_message = f"{student.student_id} - {student.name} Attendance successfully"
                    print(attendance_message)
                except TblStudents.DoesNotExist:
                    print(f"Student {stripped_name} not found in database")

            # Lưu thông tin nhận diện vào danh sách
            detection_info = {
                'name': stripped_name,
                'confidence': class_probability,
                'box': {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
            }
            detections.append(detection_info)
        
        if attendance_message:
            cv2.putText(frame, attendance_message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Ghi thông tin nhận diện ra file JSON
    with open('detections.json', 'w') as json_file:
        json.dump(detections, json_file, indent=4)

def diemdanh(request):
    with open('Face/svm_model/svm_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('Face/svm_model/out_encoder.pkl', 'rb') as encoder_file:
        out_encoder = pickle.load(encoder_file)

    realtime_face_recognition(model, out_encoder)
    return render(request, 'admin/your_template.html', {'success_message': "Điểm danh thành công."})



# import cv2
# from django.shortcuts import render
# from numpy import expand_dims
# from mtcnn.mtcnn import MTCNN
# from keras_facenet import FaceNet
# import pickle
# import json
# from datetime import datetime
# from .models import TblStudents, Attendance

# # Load FaceNet model for embedding extraction
# embedder = FaceNet()
# facenet_model = embedder.model
# detector = MTCNN()

# # Extract face embeddings from a given frame
# def get_face_embeddings(frame):
#     faces = detector.detect_faces(frame)
#     embeddings = []
#     boxes = []
#     for face in faces:
#         x1, y1, width, height = face['box']
#         x1, y1 = abs(x1), abs(y1)
#         x2, y2 = x1 + width, y1 + height
#         face_pixels = frame[y1:y2, x1:x2]
#         face_pixels = cv2.resize(face_pixels, (160, 160))
#         face_pixels = face_pixels.astype('float32')
#         mean, std = face_pixels.mean(), face_pixels.std()
#         face_pixels = (face_pixels - mean) / std
#         samples = expand_dims(face_pixels, axis=0)
#         yhat = facenet_model.predict(samples)
#         embeddings.append(yhat[0])
#         boxes.append((x1, y1, x2, y2))
#     return embeddings, boxes

# # Capture video from the webcam and make predictions
# def realtime_face_recognition(model, out_encoder):
#     cap = cv2.VideoCapture(0)
#     detections = []  # List to store detection information
#     confidence_threshold = 80.0  # Confidence threshold
#     attendance_message = ""  # Variable to store attendance message
    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         frame = cv2.flip(frame, 1)

#         face_embeddings, boxes = get_face_embeddings(frame)
        
#         for i, face_emb in enumerate(face_embeddings):
#             samples = expand_dims(face_emb, axis=0)
#             yhat_class = model.predict(samples)
#             yhat_prob = model.predict_proba(samples)
#             class_index = yhat_class[0]
#             class_probability = yhat_prob[0, class_index] * 100
#             predict_name = out_encoder.inverse_transform(yhat_class)[0]
            
#             x1, y1, x2, y2 = boxes[i]
            
#             if class_probability >= confidence_threshold:
#                 cv2.putText(frame, f'{predict_name} ({class_probability:.2f}%)', 
#                             (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

#                 # In thông báo nhận diện khuôn mặt
#                 stripped_name = predict_name.split('_', 1)[-1]
#                 print(f"Detected: {stripped_name} with {class_probability:.2f}% confidence")
                
#                 try:
#                     student = TblStudents.objects.get(name=stripped_name)
#                     print(f"Marking attendance for {stripped_name}")
#                     Attendance.objects.update_or_create(
#                         student=student,
#                         datetime=datetime.now(),
#                         defaults={'attended': True}
#                     )
#                     attendance_message = f"{student.student_id} - {student.name} Attendance successfully"
#                     print(attendance_message)
#                 except TblStudents.DoesNotExist:
#                     print(f"Student {stripped_name} not found in database")

#                 # Lưu thông tin nhận diện vào danh sách
#                 detection_info = {
#                     'name': stripped_name,
#                     'confidence': class_probability,
#                     'box': {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
#                 }
#                 detections.append(detection_info)
        
#         if attendance_message:
#             cv2.putText(frame, attendance_message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
#         cv2.imshow('Video', frame)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
    
#     cap.release()
#     cv2.destroyAllWindows()
    
#     # Ghi thông tin nhận diện ra file JSON
#     with open('detections.json', 'w') as json_file:
#         json.dump(detections, json_file, indent=4)

# def diemdanh(request):
#     with open('Face/svm_model/svm_model.pkl', 'rb') as model_file:
#         model = pickle.load(model_file)
#     with open('Face/svm_model/out_encoder.pkl', 'rb') as encoder_file:
#         out_encoder = pickle.load(encoder_file)

#     realtime_face_recognition(model, out_encoder)
#     return render(request, 'admin/your_template.html', {'success_message': "Điểm danh thành công."})






