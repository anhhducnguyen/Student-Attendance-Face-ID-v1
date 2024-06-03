# from django.contrib import admin
# from django.urls import path, include
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('signup', views.signup, name='signup'),
#     path('activate/<uidb64>/<token>', views.activate, name='activate'),
#     path('signin', views.signin, name='signin'),
#     path('signout', views.signout, name='signout'),
# ]


from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('demo', views.demo, name='demo'),
    path('run_cap_picture/', views.run_cap_picture, name='run_cap_picture'),
]
