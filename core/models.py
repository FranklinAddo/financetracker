from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = [
        ('analyst',    'Analyst'),
        ('manager',    'Manager'),
        ('accountant', 'Accountant'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='analyst')
    bio  = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Department(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ('planning',  'Planning'),
        ('active',    'Active'),
        ('on_hold',   'On Hold'),
        ('completed', 'Completed'),
    ]
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    budget      = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date  = models.DateField()
    end_date    = models.DateField(null=True, blank=True)
    department  = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    manager     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_projects')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def task_count(self):
        return self.tasks.count()

    def completed_tasks(self):
        return self.tasks.filter(status='done').count()


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low',    'Low'),
        ('medium', 'Medium'),
        ('high',   'High'),
    ]
    STATUS_CHOICES = [
        ('todo',        'To Do'),
        ('in_progress', 'In Progress'),
        ('review',      'In Review'),
        ('done',        'Done'),
    ]
    project     = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority    = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    due_date    = models.DateField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} [{self.project.title}]"


class Budget(models.Model):
    CATEGORY_CHOICES = [
        ('personnel', 'Personnel'),
        ('equipment', 'Equipment'),
        ('software',  'Software'),
        ('travel',    'Travel'),
        ('other',     'Other'),
    ]
    project     = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='budget_entries')
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=200)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    date        = models.DateField()
    created_by  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.category} - EUR{self.amount} ({self.project.title})"
