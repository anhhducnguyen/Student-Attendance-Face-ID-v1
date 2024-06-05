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
    

def home(request):
    return render(request, "authentication/index.html")

def regisImg(request):
    return render(request, "admin/registerImage.html")

def bost(request):
    return render(request, "admin/index.php")

def bost2(request):
    return render(request, "admin/index.php")

def userthem(request):
    return render(request, "admin/nguoidung.php")

def demo(request):
    # Truy vấn tất cả các bản ghi từ bảng authentication_tblstudents
    students = TblStudents.objects.all()
    # Trả về template test.html và truyền danh sách students vào template
    return render(request, "fe/test.html", {'students': students})

# def demo(request):
#     return render(request, "fe/test.html")

# def run_cap_picture(request):
#     # Mở camera
#     cap = cv2.VideoCapture(0)
    
#     # Kiểm tra xem camera có hoạt động không
#     if not cap.isOpened():
#         return HttpResponse("Failed to open camera.")

#     while True:
#         # Đọc frame từ camera
#         ret, frame = cap.read()
        
#         # Hiển thị frame
#         cv2.imshow('Captured Image', frame)
        
#         # Chờ một khoảng thời gian ngắn và lấy phím được nhấn
#         key = cv2.waitKey(1) & 0xFF

#         # Kiểm tra xem phím "q" đã được nhấn chưa
#         if key == ord('q'):
#             break

#     # Sau khi thoát khỏi vòng lặp, đóng camera
#     cap.release()
#     cv2.destroyAllWindows()

    # return HttpResponse("Camera stopped successfully.")














def run_cap_picture(request):
    def capture_images(name, save_dir='Face/dataset'):
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
            
            cv2.imshow('Capturing Images', frame)
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
        
        if len(captured_images) == 0:
            print("No images captured.")
            return

        train_images, val_images = train_test_split(captured_images, test_size=0.33, random_state=42)
        
        for i, img in enumerate(train_images):
            cv2.imwrite(os.path.join(train_dir, f'{name}_{i+1}.jpg'), img)
        for i, img in enumerate(val_images):
            cv2.imwrite(os.path.join(val_dir, f'{name}_{i+1}.jpg'), img)

    # Tên cố định bạn muốn sử dụng
    name = "dc"

    capture_images(name)
    return HttpResponse("Images captured and saved successfully.")


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
    while img_count < 2:
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
        cv2.imwrite(os.path.join(train_dir, f'{student_id}_{name.replace(" ", "")}_{i+1}.jpg'), img)
    for i, img in enumerate(val_images):
        cv2.imwrite(os.path.join(val_dir, f'{student_id}_{name.replace(" ", "")}_{i+1}.jpg'), img)


from os import listdir
from os.path import isdir
from PIL import Image
from numpy import savez_compressed, asarray
from mtcnn.mtcnn import MTCNN

# Hàm trích xuất khuôn mặt từ một ảnh
def extract_face(filename, required_size=(160, 160)):
    # Tải ảnh từ tệp
    image = Image.open(filename)
    # Chuyển đổi sang RGB nếu cần thiết
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
    # Liệt kê các tệp
    for filename in listdir(directory):
        # Đường dẫn
        path = directory + '/' + filename
        # Trích xuất khuôn mặt
        face = extract_face(path)
        # Nếu không có khuôn mặt nào được phát hiện, bỏ qua ảnh này
        if face is None:
            continue
        # Lưu trữ
        faces.append(face)
    return faces

# Hàm tải tập dữ liệu chứa một thư mục con cho mỗi lớp chứa các hình ảnh
def load_dataset(directory):
    X, y = list(), list()
    # Liệt kê các thư mục, một cho mỗi lớp
    for subdir in listdir(directory):
        # Đường dẫn
        path = directory + subdir + '/'
        # Bỏ qua các tệp có thể có trong thư mục
        if not isdir(path):
            continue
        # Tải tất cả các khuôn mặt trong thư mục con
        faces = load_faces(path)
        # Tạo nhãn
        labels = [subdir for _ in range(len(faces))]
        # Tóm tắt tiến trình
        print('>loaded %d examples for class: %s' % (len(faces), subdir))
        # Lưu trữ
        X.extend(faces)
        y.extend(labels)
    return asarray(X), asarray(y)

# Hàm chính để tải tập dữ liệu, tạo và lưu trữ nó
def main():
    # Tải tập dữ liệu huấn luyện
    trainX, trainy = load_dataset('Face/dataset_split/train/')
    print(trainX.shape, trainy.shape)

    # Tải tập dữ liệu kiểm tra
    testX, testy = load_dataset('Face/dataset_split/val/')

    # Lưu mảng vào một tệp ở định dạng nén
    savez_compressed('Face/5-celebrity-faces-dataset.npz', trainX, trainy, testX, testy)

# Gọi hàm chính
if __name__ == "__main__":
    main()



# def aa(request, student_id, name):
#     if request.method == 'GET':
#         # Render the form for capturing images
#         return render(request, 'admin/capture_image.html', {'student_id': student_id, 'name': name})
#     elif request.method == 'POST':
#         # Call the capture_images function with student_id and name
#         capture_images(student_id, name)
#         main()
#         # Render a success message
#         return HttpResponse("Images captured and saved successfully.")

def aa(request, student_id, name):
    if request.method == 'GET':
        # Render the form for capturing images
        return render(request, 'admin/capture_image.html', {'student_id': student_id, 'name': name})
    elif request.method == 'POST':
        # Call the capture_images function with student_id and name
        capture_images(student_id, name)
        # Gọi hàm create_embeddings sau khi chụp ảnh
        dataset_path = 'Face/5-celebrity-faces-dataset.npz'  # Thay bằng đường dẫn thực tế
        output_path = 'Face/5-celebrity-faces-embeddings.npz'  # Thay bằng đường dẫn thực tế
        create_embeddings(dataset_path, output_path)
        # Render a success message
        return HttpResponse("Images captured, saved, and embeddings created successfully.")




































def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        role = request.POST['role']  # Thay đổi lấy dữ liệu từ trường role
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
        myuser.last_name = role  # Lưu giá trị chức vụ vào trường last_name
        myuser.is_active = True  # Make sure the user is active
        myuser.is_staff = True  # Set staff status to True
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

# def signin(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         role = request.POST['last_name']  # Thay thế lấy dữ liệu từ trường last_name
        
#         # Kiểm tra thông tin đăng nhập
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             if user.is_active and user.last_name == role:  # Sử dụng trường last_name để kiểm tra
#                 login(request, user)
#                 fname = user.first_name
#                 messages.success(request, "Đăng nhập thành công!")
#                 return redirect('home')
#             else:
#                 messages.error(request, "Tài khoản của bạn không hoạt động hoặc chức vụ không đúng.")
#                 return redirect('signin')
#         else:
#             messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
#             return redirect('signin')

#     return render(request, "authentication/signin.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['last_name']  # Role from form data
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active and user.last_name == role:  # Verify role from database
                login(request, user)
                messages.success(request, "Đăng nhập thành công!")
                
                # Redirect based on role
                if role == 'student':
                    return redirect('home')
                elif role == 'teacher':
                    # return redirect('demo')
                    return redirect('bostt')

                else:
                    messages.error(request, "Chức vụ không hợp lệ.")
                    return redirect('signin')
            else:
                messages.error(request, "Tài khoản của bạn không hoạt động hoặc chức vụ không đúng.")
                return redirect('signin')
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
            return redirect('signin')

    return render(request, "authentication/signin.html")



def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

# Cài virtualenv
# pip show virtualenv

# Cài django
# pip install django

# Tạo admin
# python .\manage.py createsuperuser

# Chuyển cơ sở dữ liệu
# python manage.py migrate

# Chạy dự án
# python .\manage.py runserver

# Cài đặt mysql
# pip install mysql

# Cài đặt dlib
# https://github.com/z-mahmud22/Dlib_Windows_Python3.x

# Bản 3.12
# python -m pip install dlib-19.24.99-cp312-cp312-win_amd64.whl

# Cài đặt
# pip install scikit-learn










# def signin(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         pass1 = request.POST['pass1']
        
#         user = authenticate(request, username=username, password=pass1)
        
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 fname = user.first_name
#                 # Truyền fname vào context
#                 context = {
#                     'fname': fname
#                 }
#                 messages.success(request, "Đăng nhập thành công!")
#                 return render(request, 'authentication/index.html', context)  # Truyền context vào template khi render
#             else:
#                 messages.error(request, "Tài khoản của bạn không hoạt động. Vui lòng liên hệ admin.")
#                 return redirect('signin')
#         else:
#             messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
#             return redirect('signin')
    
#     return render(request, "authentication/signin.html")




