# Student-Attendance-Face-ID

# Main function


**Classroom management** Lecturers create and manage classes, add student lists to each class, update class schedules and notify students via the application.

**Face Recognition** The system uses cameras to take photos of students when entering class, the application analyzes and compares snapshots with archived data storage facilities to determine the user's identity.

**Automatic points** When successfully identified, the system will automatically update the user's identity status, lecturers can view attendance reports immediately.

**Manage data points** Attendance data storage and management system, helping students easily track and extract reports, provide statistics on student class participation.

## Student-Attendance-Face-ID Installation Instructions

### Prerequisites
Before you begin, ensure you have the following software installed:

1. [Python version 3.12](https://www.python.org/)
   - Workload: `Python`
2. [Xampp](https://www.apachefriends.org/download.html)
   - Ensure `Xampp` is running and you have the necessary credentials.
     
3. Library identification ID: OpenCV, dlib
   
4. Basic knowledge about framework `Django` (Python), JavaScript, Html, Css, 
  
### Step-by-Step Installation Guide

**Step 1.** Clone the Repository

   First, clone the repository containing the application source code.

   ```bash
   git clone https://github.com/anhhducnguyen/faceRecognition
   ```
 
**Step 2.** Install virtualenv
 ```bash
 pip show virtualenv
 ```

**Step 3.** Install dlib (I got an error when trying to `pip install dlib`, if you get an error I recommend you visit the [dlib github](https://github.com/z-mahmud22/Dlib_Windows_Python3.x) so you can install it manually according to the instructions)

**Step 4.** Install django, mysql
 ```bash
 pip install django
pip install mysql
pip install scikit-learn
 ```

**Step 5.** Transfer database
```bash
python manage.py migrate
```

**Step 6.** Create admin
```bash
python .\manage.py createsuperuser
```

**Step 7.** Run the project
 ```bash
python .\manage.py runserver
 ```
