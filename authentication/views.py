from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth import authenticate, login, logout
from .tokens import generate_token
import subprocess
from django.shortcuts import render
from django.http import HttpResponse
import cv2
import os
from sklearn.model_selection import train_test_split
from mtcnn.mtcnn import MTCNN
from .models import TblStudents
from Face.train import main
from .x import get_embedding, create_embeddings
from os import listdir
from os.path import isdir
from PIL import Image
from numpy import savez_compressed, asarray
from mtcnn.mtcnn import MTCNN
import base64
import numpy as np
    

def home(request):
    return render(request, "authentication/index.html")

def classroom(request):
    return render(request, "class/classroom_detail.html")

def regisImg(request):
    return render(request, "admin/registerImage.html")

def bost(request):
    return render(request, "admin/index.php")

def bost2(request):
    return render(request, "admin/index.php")

def userthem(request):
    return render(request, "admin/nguoidung.php")

# Function to enhance image by applying denoising and smoothing
def enhance_image(image):
    # Làm sạch nhiễu bằng Gaussian Blur
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    
    # Tăng cường độ sáng và độ tương phản
    enhanced_image = cv2.convertScaleAbs(blurred_image, alpha=1.2, beta=10)
    
    return enhanced_image

# Function to flip and rotate images to increase dataset size
def augment_images(images):
    augmented_images = []
    for image in images:
        
        # Flip image vertically
        flipped_vertical = cv2.flip(image, 1)
        augmented_images.append(flipped_vertical)
        
        # Rotate image by 15 degrees clockwise
        rows, cols, _ = image.shape
        rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), 15, 1)
        rotated_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))
        augmented_images.append(rotated_image)
        
        # Rotate image by -15 degrees counterclockwise
        rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), -15, 1)
        rotated_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))
        augmented_images.append(rotated_image)
    return augmented_images


def capture_images(student_id, name, save_dir='Face/dataset_split'):
        # Create directories if not exist
    train_dir = os.path.join(save_dir, 'train', f'{student_id}_{name.replace(" ", "")}')
    val_dir = os.path.join(save_dir, 'val', f'{student_id}_{name.replace(" ", "")}')
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    detector = MTCNN()
    img_count = 0
    captured_images = []

    print("Press 'c' to capture image. Press 'q' to quit.")
    while img_count < 10:
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
                # Enhance the captured face image
                face = enhance_image(face)
                captured_images.append(face)
                img_count += 1
                print(f"Captured image {img_count}")
        elif key & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    # Augment captured images
    augmented_images = augment_images(captured_images)
    
    # Split the images into training and validation sets
    train_images, val_images = train_test_split(augmented_images, test_size=0.33, random_state=42)
    
    for i, img in enumerate(train_images):
        cv2.imwrite(os.path.join(train_dir, f'{student_id}_{name.replace(" ", "")}_{i+1}.jpg'), img)
    for i, img in enumerate(val_images):
        cv2.imwrite(os.path.join(val_dir, f'{student_id}_{name.replace(" ", "")}_{i+1}.jpg'), img)

def aa(request, student_id, name):
    if request.method == 'GET':
        return render(request, 'admin/capture_image.html', {'student_id': student_id, 'name': name})
    elif request.method == 'POST':
        capture_images(student_id, name)
        return HttpResponse("Images captured, saved, and embeddings created successfully.")


    
def extract_face(filename, required_size=(160, 160)):
    image = Image.open(filename)
    image = image.convert('RGB')
    # Chuyển đổi sang mảng
    pixels = asarray(image)
    # Tạo bộ phát hiện, sử dụng trọng số mặc định
    detector = MTCNN()
    # Phát hiện khuôn mặt trong ảnh
    results = detector.detect_faces(pixels)
    # Kiểm tra nếu không có khuôn mặt nào được phát hiện
    if len(results) == 0:
        return None
    # Trích xuất hộp giới hạn từ khuôn mặt đầu tiên
    x1, y1, width, height = results[0]['box']
    # Sửa lỗi
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    # Trích xuất khuôn mặt
    face = pixels[y1:y2, x1:x2]
    # Thay đổi kích thước mảng thành kích thước mô hình yêu cầu
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = asarray(image)
    return face_array

# Hàm tải hình ảnh và trích xuất khuôn mặt cho tất cả hình ảnh trong một thư mục
def load_faces(directory):
    faces = list()
    for filename in listdir(directory):
        path = directory + '/' + filename
        face = extract_face(path)
        if face is None:
            continue
        faces.append(face)
    return faces

def load_dataset(directory):
    X, y = list(), list()
    for subdir in listdir(directory):

        path = directory + subdir + '/'
        if not isdir(path):
            continue

        faces = load_faces(path)
        labels = [subdir for _ in range(len(faces))]
        print('>loaded %d examples for class: %s' % (len(faces), subdir))

        X.extend(faces)
        y.extend(labels)
    return asarray(X), asarray(y)

def main():
    trainX, trainy = load_dataset('Face/dataset_split/train/')
    print(trainX.shape, trainy.shape)

    testX, testy = load_dataset('Face/dataset_split/val/')

    savez_compressed('Face/5-celebrity-faces-dataset.npz', trainX, trainy, testX, testy)

if __name__ == "__main__":
    main()


    
def embeddings(request):
    main()
    dataset_path = 'Face/5-celebrity-faces-dataset.npz' 
    output_path = 'Face/5-celebrity-faces-embeddings.npz'  
    create_embeddings(dataset_path, output_path)
    return HttpResponse("Images captured, saved, and embeddings created successfully.")

# register logout login
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        role = request.POST['role']  
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signup')
        
        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters!!")
            return redirect('signup')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!!")
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = role  
        myuser.is_active = True  
        myuser.is_staff = True 
        myuser.save()
        messages.success(request, "Your Account has been created successfully!!")
        
        return redirect('signin')
        
    return render(request, "authentication/signup.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request, 'activation_failed.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, "Logged In Sucessfully!!")
            # return render(request, "authentication/index.html",{"fname":fname})
            return render(request, "authentication/index.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')



