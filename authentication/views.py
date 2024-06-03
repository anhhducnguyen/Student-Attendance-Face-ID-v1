# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.core.mail import EmailMessage, send_mail
# from geeksforgeeks import settings
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.utils.encoding import force_str, force_bytes
# from django.contrib.auth import authenticate, login, logout
# from .tokens import generate_token

# # Create your views here.
# def home(request):
#     return render(request, "authentication/index.html")

# def signup(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         pass1 = request.POST['pass1']
#         pass2 = request.POST['pass2']
        
#         if User.objects.filter(username=username):
#             messages.error(request, "Username already exist! Please try some other username.")
#             return redirect('home')
        
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email Already Registered!!")
#             return redirect('home')
        
#         if len(username)>20:
#             messages.error(request, "Username must be under 20 charcters!!")
#             return redirect('home')
        
#         if pass1 != pass2:
#             messages.error(request, "Passwords didn't matched!!")
#             return redirect('home')
        
#         if not username.isalnum():
#             messages.error(request, "Username must be Alpha-Numeric!!")
#             return redirect('home')
        
#         myuser = User.objects.create_user(username, email, pass1)
#         myuser.first_name = fname
#         myuser.last_name = lname
#         # myuser.is_active = False
#         myuser.is_active = False
#         myuser.save()
#         messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
#         # Welcome Email
#         subject = "Welcome to GFG- Django Login!!"
#         message = "Hello " + myuser.first_name + "!! \n" + "Welcome to GFG!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnubhav Madhav"        
#         from_email = settings.EMAIL_HOST_USER
#         to_list = [myuser.email]
#         send_mail(subject, message, from_email, to_list, fail_silently=True)
        
#         # Email Address Confirmation Email
#         current_site = get_current_site(request)
#         email_subject = "Confirm your Email @ GFG - Django Login!!"
#         message2 = render_to_string('email_confirmation.html',{
            
#             'name': myuser.first_name,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
#             'token': generate_token.make_token(myuser)
#         })
#         email = EmailMessage(
#         email_subject,
#         message2,
#         settings.EMAIL_HOST_USER,
#         [myuser.email],
#         )
#         email.fail_silently = True
#         email.send()
        
#         return redirect('signin')
        
        
#     return render(request, "authentication/signup.html")


# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         myuser = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         myuser = None

#     if myuser is not None and generate_token.check_token(myuser, token):
#         myuser.is_active = True
#         myuser.save()
#         login(request, myuser)
#         messages.success(request, "Your Account has been activated!!")
#         return redirect('signin')
#     else:
#         return render(request, 'activation_failed.html')


# def signin(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         pass1 = request.POST['pass1']
        
#         user = authenticate(username=username, password=pass1)
        
#         if user is not None:
#             login(request, user)
#             fname = user.first_name
#             messages.success(request, "Logged In Sucessfully!!")
#             # return render(request, "authentication/index.html",{"fname":fname})
#         else:
#             messages.error(request, "Bad Credentials!!")
#             return redirect('home')
    
#     return render(request, "authentication/signin.html")




# def signout(request):
#     logout(request)
#     messages.success(request, "Logged Out Successfully!!")
#     return redirect('home')

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

def home(request):
    return render(request, "authentication/index.html")

def demo(request):
    return render(request, "fe/test.html")

def run_cap_picture(request):
    # Mở camera
    cap = cv2.VideoCapture(0)
    
    # Kiểm tra xem camera có hoạt động không
    if not cap.isOpened():
        return HttpResponse("Failed to open camera.")

    while True:
        # Đọc frame từ camera
        ret, frame = cap.read()
        
        # Hiển thị frame
        cv2.imshow('Captured Image', frame)
        
        # Chờ một khoảng thời gian ngắn và lấy phím được nhấn
        key = cv2.waitKey(1) & 0xFF

        # Kiểm tra xem phím "q" đã được nhấn chưa
        if key == ord('q'):
            break

    # Sau khi thoát khỏi vòng lặp, đóng camera
    cap.release()
    cv2.destroyAllWindows()

    return HttpResponse("Camera stopped successfully.")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
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
        myuser.last_name = lname
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

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(request, username=username, password=pass1)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                fname = user.first_name
                context = {
                    'fname': fname
                }
                messages.success(request, "Đăng nhập thành công!")
                return redirect('home')
            else:
                messages.error(request, "Tài khoản của bạn không hoạt động. Vui lòng liên hệ admin.")
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