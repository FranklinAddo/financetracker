from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Project, Task, Budget, Department


class RegisterForm(UserCreationForm):
    """Sign-up form — also picks a role."""
    ROLE_CHOICES = [
        ('analyst',    'Analyst'),
        ('manager',    'Manager'),
        ('accountant', 'Accountant'),
    ]
    email = forms.EmailField(required=True)
    role  = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model  = User
        fields = ['username', 'email', 'password1', 'password2', 'role']


class ProjectForm(forms.ModelForm):
    class Meta:
        model  = Project
        fields = ['title', 'description', 'status', 'budget', 'start_date', 'end_date', 'department', 'manager']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date':   forms.DateInput(attrs={'type': 'date'}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model  = Task
        fields = ['title', 'description', 'priority', 'status', 'assigned_to', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


class BudgetForm(forms.ModelForm):
    class Meta:
        model  = Budget
        fields = ['category', 'description', 'amount', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model  = Department
        fields = ['name', 'description']
