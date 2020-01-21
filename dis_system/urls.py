"""dis_system URL Configuration

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
from t_dist import views

urlpatterns = [

    path('',views.home,name='home'),
    path('login/',views.user_login,name='login'),
    path('logout/', views.user_logout,name='logout'),
    path('upload/',views.upl,name="upload"),
    path('add_std/',views.add_std,name="add_std"),
    path('register/<int:id>', views.reg,name='edit'),
    path('signup/',views.signup,name="signup"),
    path('users/',views.users,name="users"),
    path('delete/<int:id>', views.delete,name='delete'),
    path('r_set/<int:id>', views.r_set,name='r_set'),
    path('all_std/', views.all_std,name='all_std'),
    path('del_std/<int:id>', views.del_std,name='del_std'),
    path('delstd69/', views.delallstd,name='delallstd'),
    path('taken/',views.taken,name="taken"),




]
