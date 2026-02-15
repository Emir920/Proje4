from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.message_list, name='message_list'),
    path('add/', views.add_message, name='add_message'),
    path('<int:message_id>/reply/', views.add_reply, name='add_reply'),
    path('react/<int:message_id>/<str:reaction_type>/', views.react, name='react'),
    path('<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='message_list'), name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    
    # Task URLs
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<int:task_id>/update-status/', views.update_task_status, name='update_task_status'),
]
