from django.contrib import admin
from .models import TodoList, Task

@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "updated_on", "created_on")
    search_fields = ("name", "owner__username", "owner__email")
    list_filter = ("created_on", "updated_on")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "todo_list", "completed", "updated_on", "created_on")
    search_fields = ("title", "todo_list__name", "todo_list__owner__username")
    list_filter = ("completed", "created_on", "updated_on")
