"""
Beginner-friendly tests for FinanceTracker
Includes:
- Unit Tests (models)
- Integration Tests (views)
- Use Case Test (workflow)
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Project, Task
import datetime


# ─────────────────────────────
# UNIT TESTS (MODELS)
# ─────────────────────────────

class ProjectModelTest(TestCase):

    def test_project_creation(self):
        user = User.objects.create_user(username='test', password='pass')

        project = Project.objects.create(
            title='Test Project',
            start_date=datetime.date.today(),
            manager=user
        )

        self.assertEqual(project.title, 'Test Project')


class TaskModelTest(TestCase):

    def test_task_creation(self):
        user = User.objects.create_user(username='test', password='pass')

        project = Project.objects.create(
            title='Project',
            start_date=datetime.date.today(),
            manager=user
        )

        task = Task.objects.create(
            project=project,
            title='My Task'
        )

        self.assertEqual(task.title, 'My Task')


# ─────────────────────────────
# INTEGRATION TESTS (VIEWS)
# ─────────────────────────────

class AuthIntegrationTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='pass')

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'user1',
            'password': 'pass'
        })

        self.assertEqual(response.status_code, 302)  # redirect after login

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # redirected to login


class ProjectIntegrationTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user2', password='pass')
        self.client.login(username='user2', password='pass')

    def test_project_list_loads(self):
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_project(self):
        response = self.client.post(reverse('project_create'), {
            'title': 'New Project',
            'description': 'Test project',
            'status': 'planning',
            'budget': '1000',
            'start_date': '2026-01-01',
            'manager': self.user.id
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(title='New Project').exists())


# ─────────────────────────────
# USE CASE TEST (WORKFLOW)
# ─────────────────────────────

class SimpleWorkflowTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='manager', password='pass')
        self.client.login(username='manager', password='pass')

    def test_user_creates_project_and_task(self):
        # Step 1: Create project
        self.client.post(reverse('project_create'), {
            'title': 'Workflow Project',
            'description': 'Workflow test',
            'status': 'planning',
            'budget': '2000',
            'start_date': '2026-01-01',
            'manager': self.user.id
        })

        project = Project.objects.get(title='Workflow Project')

        # Step 2: Create task
        self.client.post(reverse('task_create', args=[project.id]), {
            'title': 'Task 1',
            'priority': 'medium',
            'status': 'todo'
        })

        # Step 3: Check result
        self.assertEqual(project.tasks.count(), 1)