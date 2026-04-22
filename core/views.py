from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Project, Task, Budget, Department, Profile
from .forms import RegisterForm, ProjectForm, TaskForm, BudgetForm, DepartmentForm


def register_view(request):
    """Anyone can create an account."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role=form.cleaned_data['role'])
            login(request, user)
            messages.success(request, 'Account created! Welcome.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ── DASHBOARD ─────
@login_required
def dashboard(request):
    """Home page — shows summary counts."""
    context = {
        'project_count': Project.objects.count(),
        'task_count':    Task.objects.count(),
        'my_tasks':      Task.objects.filter(assigned_to=request.user)[:5],
        'recent_projects': Project.objects.order_by('-created_at')[:5],
    }
    return render(request, 'core/dashboard.html', context)

# ── PROJECTS ─────
@login_required
def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'core/project_list.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks   = project.tasks.all()
    budgets = project.budget_entries.all()
    total_spent = sum(b.amount for b in budgets)
    return render(request, 'core/project_detail.html', {
        'project': project, 'tasks': tasks,
        'budgets': budgets, 'total_spent': total_spent,
    })

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project created!')
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'core/project_form.html', {'form': form, 'action': 'Create'})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated!')
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'core/project_form.html', {'form': form, 'action': 'Edit'})

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted.')
        return redirect('project_list')
    return render(request, 'core/confirm_delete.html', {'object': project, 'type': 'Project'})

# ── TASKS ─────
@login_required
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, 'Task added!')
            return redirect('project_detail', pk=project_pk)
    else:
        form = TaskForm()
    return render(request, 'core/task_form.html', {'form': form, 'project': project, 'action': 'Create'})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated!')
            return redirect('project_detail', pk=task.project.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'core/task_form.html', {'form': form, 'project': task.project, 'action': 'Edit'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project_pk = task.project.pk
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted.')
        return redirect('project_detail', pk=project_pk)
    return render(request, 'core/confirm_delete.html', {'object': task, 'type': 'Task'})


# ── BUDGET ────
@login_required
def budget_add(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.project    = project
            entry.created_by = request.user
            entry.save()
            messages.success(request, 'Budget entry added!')
            return redirect('project_detail', pk=project_pk)
    else:
        form = BudgetForm()
    return render(request, 'core/budget_form.html', {'form': form, 'project': project})

# ── DEPARTMENTS ─────
@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'core/department_list.html', {'departments': departments})

@login_required
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created!')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'core/department_form.html', {'form': form, 'action': 'Create'})
