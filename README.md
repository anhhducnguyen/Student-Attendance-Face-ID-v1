#Main function
## Login and manage account:

- Students and trainees can log in to the system with their personal accounts.
- Lecturers can manage class information, students and class schedules.

## Classroom management:
- Lecturers create and manage classes, add student lists to each class.
- Update class schedules and notify students via the application.

## Face Recognition:
- The system uses cameras to take photos of students when entering class.
- The application analyzes and compares snapshots with archived data storage facilities to determine the user's identity.

##Automatic points:
- When successfully identified, the system will automatically update the user's identity status.
- Lecturers can view attendance reports immediately.

## Manage data points:
- Attendance data storage and management system, helping students easily track and extract reports.
- Provide statistics on student class participation.

## Notifications and reminders:
- Send notifications about class schedules and related changes to students.
- Remind students about attendance if they forget.

# Technology used
- Language installer: Python, JavaScript, Html, Css
- Web framework: Django (Python)
- Database: MySQL
- Library identification ID: OpenCV, dlib
- Deployment: Docker, Kubernetes
- Authentication: JWT (JSON Web Token) or OAuth2

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
python .\manage.py createsuperuser
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
https://github.com/z-mahmud22/Dlib_Windows_Python3.x
 ```

- Bản python 3.12
```bash
python -m pip install dlib-19.24.99-cp312-cp312-win_amd64.whl
```
- Cài đặt
 ```bash
pip install scikit-learn
 ```
