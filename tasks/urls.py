from django.urls import path
from .views import register
from django.contrib.auth import views as auth_views

from .views import (
    DashboardView,
    AdminDashboardView,
    WorkspaceListView,
    WorkspaceDetailView,
    WorkspaceCreateView,
    WorkspaceUpdateView,
    WorkspaceDeleteView,
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView,
    TaskStatusUpdateView,
)

urlpatterns = [

    
    path('', DashboardView.as_view(), name='dashboard'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
     path('register/', register, name='register'),  # Ensure this URL is correctly mapped
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('workspaces/', WorkspaceListView.as_view(), name='workspace_list'),
    path('workspaces/<int:pk>/', WorkspaceDetailView.as_view(), name='workspace_detail'),
    path('workspaces/create/', WorkspaceCreateView.as_view(), name='workspace_create'),
    path('workspaces/update/<int:pk>/', WorkspaceUpdateView.as_view(), name='workspace_update'),
    path('workspaces/delete/<int:pk>/', WorkspaceDeleteView.as_view(), name='workspace_delete'),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/update/<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('tasks/delete/<int:pk>/', TaskDeleteView.as_view(), name='task_delete'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('api/task-status-update/<int:task_id>/', TaskStatusUpdateView.as_view(), name='task_status_update'),
]
