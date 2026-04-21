from django.contrib import admin
from .models import Profile, Department, Project, Task, Budget

admin.site.register(Profile)
admin.site.register(Department)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Budget)
