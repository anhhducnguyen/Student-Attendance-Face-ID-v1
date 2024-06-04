# GFG---Django-Login-System

# Chức năng chính
## Đăng nhập và quản lý tài khoản:

- Sinh viên và giảng viên có thể đăng nhập vào hệ thống bằng tài khoản cá nhân.
- Giảng viên có thể quản lý thông tin lớp học, sinh viên và lịch học.

## Quản lý lớp học:
- Giảng viên tạo và quản lý các lớp học, thêm danh sách sinh viên vào từng lớp.
- Cập nhật lịch học và thông báo cho sinh viên qua ứng dụng.

## Nhận diện khuôn mặt:
- Hệ thống sử dụng camera để chụp ảnh sinh viên khi họ vào lớp.
- Ứng dụng phân tích và so sánh khuôn mặt chụp được với cơ sở dữ liệu đã lưu trữ để xác định danh tính sinh viên.

## Điểm danh tự động:
- Khi nhận diện thành công, hệ thống tự động cập nhật trạng thái điểm danh của sinh viên.
- Giảng viên có thể xem báo cáo điểm danh ngay lập tức.

## Quản lý dữ liệu điểm danh:
- Hệ thống lưu trữ và quản lý dữ liệu điểm danh, giúp giảng viên dễ dàng theo dõi và trích xuất báo cáo.
- Cung cấp thống kê về tình hình tham gia lớp học của sinh viên.

## Thông báo và nhắc nhở:
- Gửi thông báo về lịch học và các thay đổi liên quan đến sinh viên.
- Nhắc nhở sinh viên về việc điểm danh nếu họ quên.

# Công nghệ sử dụng
- Ngôn ngữ lập trình: Python, JavaScript, Html, Css
- Framework web: Django (Python)
- Cơ sở dữ liệu: MySQL
- Thư viện nhận diện khuôn mặt: OpenCV, dlib
- Triển khai: Docker, Kubernetes
- Xác thực: JWT (JSON Web Token) hoặc OAuth2

# Cài đặt
- Cài virtualenv
 ```bash
 pip show virtualenv
 ```
- Cài django
 ```bash
 pip install django
 ```

- Tạo admin
```bash
python .\manage.py createsuperuse
```
- Cài django
 ```bash
 pip install django
 ```

- Chuyển cơ sở dữ liệu
```bash
python manage.py migrate
```
- Chạy dự án
 ```bash
python .\manage.py runserver
 ```

- Cài đặt mysql
```bash
pip install mysql
```
- Cài đặt dlib
 ```bash
[python .\manage.py runserver](https://github.com/z-mahmud22/Dlib_Windows_Python3.x)
 ```

- Bản python 3.12
```bash
python -m pip install dlib-19.24.99-cp312-cp312-win_amd64.whl
```
- Cài đặt
 ```bash
pip install scikit-learn
 ```
