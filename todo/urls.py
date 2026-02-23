from django.urls import path
from .views import (
    TodoListIndexView,
    TodoListCreateView,
    TodoListDetailView,
    TodoListUpdateView,
    TodoListDeleteView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    ProfileView,
    UsernameUpdateView,
)

app_name = "todo"

urlpatterns = [
    path("lists/", TodoListIndexView.as_view(), name="list_index"),
    path("lists/new/", TodoListCreateView.as_view(), name="list_create"),
    path("lists/<int:pk>/", TodoListDetailView.as_view(), name="list_detail"),

    # List edit/delete
    path("lists/<int:pk>/edit/", TodoListUpdateView.as_view(), name="list_update"),
    path("lists/<int:pk>/delete/", TodoListDeleteView.as_view(), name="list_delete"),

    # Tasks
    path("lists/<int:pk>/tasks/new/", TaskCreateView.as_view(), name="task_create"),
    path(
        "lists/<int:list_pk>/tasks/<int:task_pk>/edit/",
        TaskUpdateView.as_view(),
        name="task_edit",
    ),
    path(
        "lists/<int:list_pk>/tasks/<int:task_pk>/delete/",
        TaskDeleteView.as_view(),
        name="task_delete",
    ),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/username/", UsernameUpdateView.as_view(), name="profile_username"),
]