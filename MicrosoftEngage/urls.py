"""MicrosoftEngage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from classroom import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register, name='register'),
    path('register/studentregister/', views.studentRegister, name='studentRegister'),
    path('register/teacherregister/', views.teacherRegister, name='teacherRegister'),
    path('slot/', views.viewClassSlots ,name='viewClassSlots'),
    path('slot/create/', views.createClassSlot, name='createClassSlot'),
    path('slot/edit/<int:class_slot_id>/', views.editClassSlot, name='editClassSlot'),
    path('slot/delete/<int:class_slot_id>/', views.deleteClassSlot, name='deleteClassSlot'),
    path('slot/book/', views.bookClassSlot, name='bookClassSlot'),
    path('groupdiscussion/', views.viewGroupDiscussion, name='viewGroupDiscussion'),
    path('groupdiscussion/create/', views.createGroupDiscussion, name='createGroupDiscussion'),
    path('groupdiscussion/join/<int:gd_slot_id>/',views.joinGroupDiscussion,name="joinGroupDiscussion"),
    path('timeline/', views.timeline, name='timeline'),
]
