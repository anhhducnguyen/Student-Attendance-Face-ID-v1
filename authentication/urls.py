from django.contrib import admin
from django.urls import path
from . import views
from . import dashboardController

urlpatterns = [
    # views
    path('', views.home, name='home'),
    # path('', views.bost, name='bost'),
    path('bostt', views.bost2, name='bostt'),
    path('nguoidung', views.userthem, name='nguoidung'),

    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('run_cap_picture/', views.run_cap_picture, name='run_cap_picture'),
    # dashboardController
    path('demo', dashboardController.demo, name='demo'),
    # path('ok', dashboardController.ok, name='ok'),

    # test data
    # path('', dashboardController.data, name='students-view'),
    path('test', dashboardController.data, name='students-view'),
    path('add_student/', dashboardController.add_student, name='add_student'),
    path('update_student/<int:student_id>/', dashboardController.update_student, name='update_student'),
    path('delete_student/<int:student_id>/', dashboardController.delete_student, name='delete_student'),
   
]
