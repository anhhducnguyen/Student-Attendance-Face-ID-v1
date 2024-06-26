# Student-Attendance-Face-ID

**Classroom management:** Lecturers create and manage classes, add student lists to each class, update class schedules and notify students via the application.

**Face Recognition:** The system uses cameras to take photos of students when entering class, the application analyzes and compares snapshots with archived data storage facilities to determine the user's identity.

**Automatic points:** When successfully identified, the system will automatically update the user's identity status, lecturers can view attendance reports immediately.

**Manage data points:** Attendance data storage and management system, helping students easily track and extract reports, provide statistics on student class participation.

## MTCNN architecture

Face detection (P-Net)

Estimation of facial landmark locations (R-Net)

Extracting facial features (O-Net)

## Facenet is used for the following tasks:

**Face Recognition:** Determine the identity of a fish from a database of known faces.

**Face Verification:** Verify viewing two photos whether the face belongs to the same person or not.

**Face Clustering:** Group face photos together based on similarity, without prior knowledge of identity

## SVM structure

Main characteristics:

**Classification:** Find the best hyperplane to classify divide the data into classes, maximizing the distance to these nearest data points (support vectors).

**Kernel:** Use kernel functions to process data Linear, helps classify complex data.

## Training Process and Data

**Quantity:** 30 photos per label
- 20 Train photos
- 10 Val photos

**Number of labels ( Class ):** Custom

**Photo size:** 160x160px

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

## Evaluate the model over time


## <div align="left">Contact</div>

To report bugs and request features of software, please contact me for questions and discussion!

<br>
<div align="center">
  <a href="#"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-github.png" width="3%" alt="Ultralytics GitHub"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="#"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-linkedin.png" width="3%" alt="Ultralytics LinkedIn"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="#"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-twitter.png" width="3%" alt="Ultralytics Twitter"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="#"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-youtube.png" width="3%" alt="Ultralytics YouTube"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="#"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-tiktok.png" width="3%" alt="Ultralytics TikTok"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="#"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-instagram.png" width="3%" alt="Ultralytics Instagram"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="#"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-discord.png" width="3%" alt="Ultralytics Discord"></a>
</div>



