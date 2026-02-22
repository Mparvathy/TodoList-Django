from django.urls import path,include
from. import views


urlpatterns = [
          path('', views.home, name='home'),
          path('adminclick/', views.adminclick, name='adminclick'),
          path('userclick/', views.userclick, name='userclick'),
          path('userignup/', views.userignup, name='userignup'),  
          path('userlogin/', views.user_login, name='userlogin'),
          path('logout/', views.user_logout, name='logout'),
          path('userdashboard/', views.userdashboard, name='userdashboard'),
          path('add-task/', views.add_task, name='add_task'),
          path('tasks/running/', views.running_tasks, name='running_tasks'),
          path('task/delete/<int:task_id>/', views.delete_task, name='delete_task'),
          path('tasks/completed/', views.completed_tasks, name='completed_tasks'),
          path('task/edit/<int:task_id>/', views.edit_task, name='edit_task'),
          path('change-password/', views.change_password, name='change_password'),
          path('adminignup/', views.adminsignup, name='adminsignup'),  
          path('adminlogin/', views.admin_login, name='adminlogin'),
          path('admindashboard/', views.admindashboard, name='admindashboard'),
          path('add-category/', views.add_category, name='add_category'),
          path('profile/', views.profile, name='profile'),
          path('adminlogout/', views.admin_logout, name='adminlogout'),
          path('task/complete/<int:task_id>/', views.complete_task, name='complete_task'),
          path('tasks/', views.admin_tasks_users, name='admin_tasks_users'),
          path('tasks/<int:user_id>/', views.admin_user_tasks, name='admin_user_tasks'),
          path('verify-otp/', views.verify_otp, name='verify_otp'),

]
