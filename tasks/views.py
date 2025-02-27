import json
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.views.generic.edit import FormMixin
from django.views.decorators.http import require_http_methods
from .models import Task, Workspace, Notification
from .forms import TaskForm, WorkspaceForm

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/dashboard.html'
    # ... (existing code)

class AdminDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'tasks/admin_dashboard.html'
    # ... (existing code)

class WorkspaceListView(LoginRequiredMixin, ListView):
    model = Workspace
    template_name = 'tasks/workspace_list.html'
    context_object_name = 'workspaces'

    def get_queryset(self):
        return Workspace.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)
        ).distinct()

class WorkspaceDetailView(LoginRequiredMixin, DetailView):
    model = Workspace
    template_name = 'tasks/workspace_detail.html'
    context_object_name = 'workspace'

    def get_queryset(self):
        return Workspace.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workspace = self.get_object()
        
        context['tasks'] = Task.objects.filter(workspace=workspace)
        context['members'] = workspace.members.all()
        context['is_owner'] = workspace.owner == self.request.user
        
        return context

class WorkspaceCreateView(LoginRequiredMixin, CreateView):
    model = Workspace
    form_class = WorkspaceForm
    template_name = 'tasks/workspace_form.html'
    success_url = reverse_lazy('workspace_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        form.instance.members.add(self.request.user)
        messages.success(self.request, 'Workspace created successfully!')
        return response

class WorkspaceUpdateView(LoginRequiredMixin, UpdateView):
    model = Workspace
    form_class = WorkspaceForm
    template_name = 'tasks/workspace_form.html'
    success_url = reverse_lazy('workspace_list')

    def get_queryset(self):
        return Workspace.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Workspace updated successfully!')
        return super().form_valid(form)

class WorkspaceDeleteView(LoginRequiredMixin, DeleteView):
    model = Workspace
    template_name = 'tasks/workspace_confirm_delete.html'
    success_url = reverse_lazy('workspace_list')

    def get_queryset(self):
        return Workspace.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Workspace deleted successfully!')
        return super().delete(request, *args, **kwargs)

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(
            Q(assigned_to=self.request.user) | Q(created_by=self.request.user)
        ).select_related('workspace', 'created_by', 'assigned_to')

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(
            Q(assigned_to=self.request.user) | Q(created_by=self.request.user)
        )

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        
        # Create notification for assigned user
        if form.instance.assigned_to != self.request.user:
            Notification.objects.create(
                user=form.instance.assigned_to,
                task=form.instance,
                message=f'You have been assigned a new task: {form.instance.title}'
            )
        
        messages.success(self.request, 'Task created successfully!')
        return response

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(
            Q(created_by=self.request.user) |
            Q(workspace__owner=self.request.user)
        )

    def form_valid(self, form):

        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(
            Q(created_by=self.request.user) |
            Q(workspace__owner=self.request.user)
        )

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Task deleted successfully!')
        return super().delete(request, *args, **kwargs)

class TaskStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['status']
    http_method_names = ['post']

    def get_queryset(self):
        return Task.objects.filter(
            Q(assigned_to=self.request.user) |
            Q(created_by=self.request.user) |
            Q(workspace__owner=self.request.user)
        )

    def form_valid(self, form):
        messages.success(self.request, 'Task status updated successfully!')
        return super().form_valid(form)



def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            messages.success(request, "Account created successfully!")
            return redirect('dashboard')  # Redirect to dashboard or another page
    else:
        form = UserRegisterForm()
    
    return render(request, 'register.html', {'form': form})