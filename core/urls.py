from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('',         views.dashboard,    name='dashboard'),
    path('register/',views.register_view,name='register'),
    path('login/',   views.login_view,   name='login'),
    path('logout/',  views.logout_view,  name='logout'),

    # Projects
    path('projects/',              views.project_list,   name='project_list'),
    path('projects/new/',          views.project_create, name='project_create'),
    path('projects/<int:pk>/',     views.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit/',views.project_edit,   name='project_edit'),
    path('projects/<int:pk>/delete/',views.project_delete,name='project_delete'),

    # Tasks (under a project)
    path('projects/<int:project_pk>/tasks/new/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/',   views.task_edit,   name='task_edit'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),

    # Budget
    path('projects/<int:project_pk>/budget/add/', views.budget_add, name='budget_add'),

    # Departments
    path('departments/',     views.department_list,   name='department_list'),
    path('departments/new/', views.department_create, name='department_create'),
]
